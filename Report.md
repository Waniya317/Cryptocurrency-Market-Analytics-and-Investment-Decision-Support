# Final Architecture and FinOps Report
Cryptocurrency Market Analytics and Investment Decision Support

**Team:** Khushbakht (Member 1), Waniya (Member 2)
**Platform:** Databricks Free Edition, PySpark, Delta Lake, Power BI
**Repo:** https://github.com/Waniya317/Cryptocurrency-Market-Analytics-and-Investment-Decision-Support
**Date:** <date>

## 1. Project summary
Pipeline that ingests hourly CoinGecko data for 94 cryptocurrencies, cleans it, models it
as a star schema and serves a Power BI dashboard for decision support (no automatic
investment decisions). Phase 1: data collection scripts. Phase 2: Bronze and Silver.
Phase 3: Gold, automation, BI, this report.

Business questions answered (from the Phase 1 proposal):
1 Performance over time | 2 Market cap vs trading activity | 3 Volatility |
4 Day-of-week differences | 5 Hour-of-day differences | 6 Volume changes vs price moves |
7 Recent intraday behavior | 8 Recent vs historical behavior | 9 Predicted direction (optional) |
10 Model accuracy (optional) | 11 Allocation scenarios under market conditions

## 2. Architecture
[Insert docs/architecture.png]
Flow: CoinGecko JSON (Phase 1 scripts) -> Unity Catalog Volume -> Bronze (raw + metadata)
-> Silver (typed, validated, deduplicated) -> Gold (star schema) -> Power BI (direct
connection to a Databricks SQL warehouse).
Cross-cutting: crypto.ops.pipeline_execution_logs, crypto.bronze.quarantine,
orchestrator notebook (12_pipeline_orchestrator).
Source note: the CoinGecko API is blocked on Databricks Free Edition, so the scripts
collected the JSON beforehand and the professor approved manual ingestion.

| Layer | Table(s) | Rows | Notes |
|---|---|---|---|
| Bronze | crypto.bronze.market_data_raw | 66,401 | 94 coins, key (coin_id, ts_ms), explicit schema, load_timestamp |
| Quarantine | crypto.bronze.quarantine | 0 | Records with extra/missing keys or null key/price |
| Silver | crypto.silver.market_data_clean | 66,401 | key (coin_id, event_ts), event_date, event_hour added |
| Gold | crypto.gold.* | <fill> | See section 3 |
| Logs | crypto.ops.pipeline_execution_logs | <fill> | One row per run |

## 3. Gold data model
Star schema with 4 dimensions (dim_coin, dim_date, dim_hour, dim_scenario), 1 bridge
(bridge_scenario_coin) and 3 facts (fact_market_hourly, fact_coin_daily, fact_portfolio_daily).
[Insert ER diagram image from docs/GOLD_DATA_MODEL.md]
Grains: fact_market_hourly = coin x hour, fact_coin_daily = coin x day,
fact_portfolio_daily = scenario x day. Full dictionary and the mapping of each business
question to its table: docs/GOLD_DATA_MODEL.md.
Refresh: facts recomputed from Silver and merged (MERGE INTO, update only when values
changed); the orchestrator runs this after every Silver update.
Optimization: liquid clustering plus OPTIMIZE. Before/after evidence:
[Insert docs/screenshots/optimize_before_after.png]
| Metric | Before OPTIMIZE | After OPTIMIZE |
|---|---|---|
| Number of files (fact_market_hourly) | <fill> | <fill> |
| Query time, coin + date filter | <fill> | <fill> |

## 4. Decision log
| Decision | Why |
|---|---|
| Explicit StructType schemas, no inferSchema | Phase 2 requirement; predictable types, no surprises when files change |
| Business key (coin_id, ts_ms) and MERGE INTO | Unique per coin per hour; re-runs report inserted=0, updated=0 (proven in PIPELINE_RUN_LOG.md) |
| No partitioning; liquid clustering on key columns | About 81k rows is far too small for partitions (many tiny files). Queries filter by coin and date, so clustering on those keys gives data skipping without a rigid layout |
| Deterministic surrogate key coin_key = xxhash64(coin_id) | Identity columns change on re-run and break idempotent MERGE |
| Two coin-level facts (hourly and daily) | Hourly serves intraday questions (5-8); the daily aggregate serves performance and risk (1-4) without scanning hourly rows |
| fact_portfolio_daily + dim_scenario + bridge | Needed for question 11: allocation scenarios evaluated per day and market condition |
| Backfill by date range (05) | Reprocess Bronze to Silver for a chosen period |
| Gold recomputed from Silver then merged | Data is small, so simple and idempotent. At enterprise scale: watermark or Change Data Feed |
| Schema drift | Records whose keys differ from the expected set go to crypto.bronze.quarantine with the reason, instead of failing the load. <Describe the drift test: a small JSON with an extra key was loaded, N rows quarantined, the good rows loaded. The real source files had 0 drift records> |
| PII | None. The data is public market data (coin IDs, prices, volumes), so no masking was needed. The Databricks access token used by Power BI is stored only in Power BI credentials and is never committed to GitHub. In production, access would be governed with Unity Catalog grants |
| Silver price rule | <price >= 0 or price > 0, final decision and why> |
| Orchestrator notebook | Requirement: Gold refreshes automatically after Silver; one run executes 03, 04, 09, 10 and logs the whole run |
| Two Databricks workspaces | Free Edition is one user per workspace; GitHub is the shared source of truth, Power BI connects to Waniya's workspace |

## 5. Spark UI and DAG analysis

Most complex transformation: the fact_coin_daily aggregation in 10_gold_facts
(Silver -> window functions -> daily aggregate). Plan captured with df.explain("formatted").

[Insert screenshot: Query Profile of the fact_coin_daily MERGE from the notebook run]

Physical plan, read bottom to top:
| Step | Operator | What it does |
|---|---|---|
| 1 | PhotonScan parquet crypto.silver.market_data_clean | Reads the Silver Delta table (parquet files) |
| 2-4 | PhotonShuffleExchange (Sink/Source) | SHUFFLE 1: rows are redistributed by coin_id so all hours of one coin are on the same partition |
| 5 | PhotonSort | Sorts each coin's rows by event_ts, needed for lag() |
| 6 | PhotonWindow | Window functions per coin: previous price and previous volume (lag), plus mean and std dev of volume for the volume-spike flag |
| 7 | PhotonProject | Computes hourly_return_pct, volume_change_pct, volume_to_mcap_ratio, coin_key and date_key |
| 8 | PhotonGroupingAgg (partial) | Map-side aggregation per (coin_key, date_key) BEFORE the shuffle, which shrinks the data that must move |
| 9-11 | PhotonShuffleExchange (Sink/Source) | SHUFFLE 2: partial aggregates for the same (coin_key, date_key) are brought together |
| 12 | PhotonGroupingAgg (final) | open/close price (min_by/max_by on event_ts), high, low, averages, volatility (std dev), hours_count |
| 13 | PhotonProject | Computes daily_return_pct, intraday_range_pct and load_timestamp |
| 14-15 | PhotonColumnarToRow, ResultStage | Returns the result to the MERGE |

Key points:
- Shuffles: 2 (stage boundaries "ShuffleMapStage"). Shuffle 1 is required because window
  functions need each coin's rows together and ordered; shuffle 2 is required for the
  group-by on (coin_key, date_key). Shuffles are the most expensive operations in Spark.
- Partial then final aggregation (steps 8 and 12) is the standard two-phase aggregate;
  it reduces the data crossing shuffle 2.
- Photon: every operator runs in the vectorised Photon engine (the "Photon" prefix),
  which is why the plan has no row-based Spark operators until the final ColumnarToRow.
- AdaptiveSparkPlan: Adaptive Query Execution is on, so shuffle partition counts are
  adjusted at run time. With about 66,000 rows most shuffle partitions are tiny, and AQE
  coalesces them.
- Predicate pushdown: this refresh reads the whole Silver table with no WHERE clause, so
  there is no filter to push down. Pushdown and data skipping apply to the dashboard
  queries (filter by coin_key and date_key), where liquid clustering lets Spark skip
  files. Evidence: <paste PushedFilters from explain of the query in 11_gold_optimize>.
- Why not avoid the first shuffle: the window needs per-coin ordering; at this data size
  the cost is negligible, and at enterprise scale Silver could be clustered by coin_id.
## 6. Dashboard
[Insert screenshots: Market Overview, Risk and Performance, Intraday Analysis,
Decision Support, Pipeline Monitoring]
[Insert Power BI Model view screenshot: one-to-many relationships dimension -> fact]
Pages and the questions they answer are listed in docs/logs/VISUALIZATION_LOG.md.
Pipeline Monitoring page uses the audit table (runs by layer and status, rows and
duration per run) and the quarantine table (error reasons, failed runs).

## 7. Validation and data quality
Phase 2 (07_validation_checks): Bronze 66,401 = Silver 66,401, 0 duplicate keys,
0 invalid values, 0 quarantined.
Phase 3 (13_gold_validation): foreign keys resolve (0 orphans), 0 duplicate keys in every
Gold table, row counts reconcile to Silver. <fill results>

## 8. Cost and FinOps
Free Edition has no billing data, so cost is estimated from measured runtimes.
Measured from pipeline_execution_logs:
| Run | Duration (s) | Rows read | Rows written |
|---|---|---|---|
| Orchestrator, typical incremental run | <fill> | <fill> | <fill> |
| Gold facts only | <fill> | <fill> | <fill> |

Formula: cost per run = duration (hours) x DBU per hour x price per DBU.
Assumptions (check the current Databricks pricing page): DBU per hour = <x>,
price per DBU = <y> USD.
- Typical daily incremental run: <fill> USD.
- Enterprise scenario, hourly for one year: 8,760 runs x <cost per run> = <fill> USD,
  plus storage (a few MB, negligible here).
Optimizations:
- Use job compute (not all-purpose) with auto-termination between runs.
- Process only new data (Auto Loader, watermark or Change Data Feed) instead of rescanning.
- Run OPTIMIZE daily or weekly, not hourly.
- Trigger runs on file arrival when data is irregular, instead of a fixed hourly schedule.
- Right-size the cluster; enable Photon only if the speed-up outweighs its DBU premium.

## 9. Limitations and future work
- Only about 31 days of data: day-of-week results have about 4 samples per weekday and
  market conditions are short-term, so results are indicative.
- The incremental file fully overlaps the full load, so it inserted 0 rows; a controlled
  test shows incremental inserts and updates.
- Optional prediction component (questions 9 and 10): <implemented / future work>.
- Future work: streaming ingestion, Unity Catalog access controls, scheduled Databricks Job.
