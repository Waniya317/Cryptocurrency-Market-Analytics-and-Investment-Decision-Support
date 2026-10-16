# Project Plan: Cryptocurrency Market Analytics and Investment Decision Support

**Team:** Khushbakht (Member 1), Waniya (Member 2)
**Platform:** Databricks Free Edition, PySpark, Delta Lake, Power BI
**Source:** Existing CoinGecko JSON files (manual ingestion approved by professor)
**Repo:** https://github.com/Waniya317/Cryptocurrency-Market-Analytics-and-Investment-Decision-Support
**Last updated:** 2026-10-16

## Architecture
Raw JSON (Volume) -> Bronze (Delta) -> Silver (Delta) -> Gold (star schema) -> Power BI

## Environment
- Catalog: crypto | Schemas: bronze, silver, gold, ops
- Volume: /Volumes/crypto/bronze/raw_files/ (both JSON files directly inside)
- Tables: crypto.bronze.market_data_raw, crypto.bronze.quarantine,
  crypto.silver.market_data_clean, crypto.ops.pipeline_execution_logs, crypto.gold.*

## Phase 1 Recap (DONE)
- 94 valid coins from ~100 IDs
- Full load: 30 days hourly, 66,401 observations
- Incremental load: 7 days hourly, 14,474 observations
- Fields: coin ID, timestamp, price, market cap, total volume

## Business Questions (from Phase 1 proposal)
1. How have major cryptocurrencies performed over time?
2. How do the selected cryptocurrencies compare in market capitalization and trading activity?
3. Which cryptocurrencies have historically experienced greater volatility?
4. How does performance differ across days of the week?
5. How does market activity differ across hours of the day?
6. Are significant changes in trading volume associated with major price movements?
7. What is the recent intraday market behavior of each cryptocurrency?
8. How does recent intraday behavior compare with historical patterns?
9. What is the model's predicted direction for the next observation or day (if implemented)?
10. How accurate has the model been on unseen data (if implemented)?
11. How would different allocations have performed under different market conditions?
The dashboard provides decision support, not automatic investment decisions.

==================== PHASE 2 (COMPLETE): Bronze + Silver ====================

## Phase 2 Goal
Build a Bronze and Silver pipeline that is idempotent, parameterized,
logged, and schema-safe.

## Phase 2 Tasks
| Phase | Task | Owner | Output | Status |
|---|---|---|---|---|
| A | Databricks setup | Khushbakht | Workspace ready | DONE |
| A2 | Waniya's workspace + JSON upload | Waniya | Workspace ready | DONE |
| B | Explicit schemas + config | Khushbakht | 00_config_schemas | DONE |
| C | Logging table + helpers | Khushbakht | 01_logging_utils | DONE |
| D | Bronze full load | Khushbakht | 02_bronze_full_load | DONE |
| E | Bronze incremental load | Khushbakht | 03_bronze_incremental | DONE |
| F | Silver transform | Waniya | 04_silver_transform | DONE |
| G | Backfill parameters | Waniya | 05_backfill_runner | DONE |
| H | Schema drift / quarantine | Waniya | 06_schema_drift_quarantine | DONE |
| I | Validation checks | Waniya | 07_validation_checks | DONE |
| J | Data model docs | Waniya | DATA_MODEL.md | DONE |
| K | README + final push | Khushbakht | README.md | Moved to Phase 3 (P16) |
| L | Idempotency proof (Bronze) | Khushbakht | PIPELINE_RUN_LOG.md + screenshots | DONE |
| L2 | Idempotency proof (Silver) | Waniya | PIPELINE_RUN_LOG.md | DONE |
| M | Bronze notebooks pushed to GitHub | Khushbakht | src/pyspark/ 00-03 | DONE |
| N | All MD docs + screenshots uploaded to GitHub | Khushbakht | docs/ | DONE |
| O | PR review: Bronze -> main | Waniya | Merged PR | DONE |

## Phase 2 Requirement Checklist
- [x] Databricks Free Edition used
- [x] All PySpark code for Bronze and Silver available in GitHub
- [x] Explicit StructType/StructField schemas used (no inferSchema)
- [x] Bronze and Silver columns, types, keys documented in DATA_MODEL.md
- [x] load_timestamp included in Bronze and Silver schemas
- [x] Idempotent processing via Delta MERGE INTO (proof in PIPELINE_RUN_LOG.md)
- [x] Parameterized loads (path, batch_id widgets) and backfill by date range
- [x] Schema drift detected and quarantined (crypto.bronze.quarantine)
- [x] pipeline_execution_logs created and populated
- [ ] README updated (data models + how to run): moved to Phase 3 (P16)
- Known follow-ups (tracked as E004, E005, fixed in P0): price rule wording in
  DATA_MODEL vs Silver code, missing row counts for R006/R007.

## Phase 2 Results
Bronze 66,401 rows, 94 coins, 0 quarantined. Silver 66,401 rows, 0 duplicate keys.
Re-runs of Bronze and Silver report inserted=0, updated=0.

## Phase 2 Risks
| Risk | Mitigation |
|---|---|
| CoinGecko API blocked in Databricks | Manual JSON upload (approved) |
| Duplicate rows on re-run | MERGE INTO on (coin_id, ts_ms), update only if values changed |
| Schema changes in JSON | Records with different keys go to crypto.bronze.quarantine |
| Free Edition limits | Small data (~81k rows), avoid heavy jobs |
| Two separate workspaces | Same names, same notebooks via GitHub |
| %run fails when pasted as a comment | Keep %run alone in its own cell |
| Stale or conflicting docs | GitHub is the single source of truth, logs are append-only |

==================== PHASE 3 (IN PROGRESS): Gold + BI + Report ====================

## Phase 3 Goal
Business-ready Gold star schema, automated Bronze->Silver->Gold run, Power BI
dashboard on the Gold layer, and a final architecture + FinOps PDF report.

## Phase 3 Tasks (notebooks in sequence)
| ID | Task | Owner | Output | Status |
|---|---|---|---|---|
| P0 | Fix Phase 2 loose ends (price rule, R006/R007 counts, screenshot names) | Waniya | Docs matched to code | TODO |
| P1 | Gold DDL + liquid clustering | Khushbakht | 08_gold_setup | TODO |
| P2 | Gold dimensions + scenario bridge | Khushbakht | 09_gold_dimensions | TODO |
| P3 | Gold facts (hourly, daily, portfolio) with MERGE + logging | Khushbakht | 10_gold_facts | TODO |
| P4 | OPTIMIZE + before/after evidence | Khushbakht | 11_gold_optimize | TODO |
| P5 | Gold data dictionary + ER diagram | Khushbakht | docs/GOLD_DATA_MODEL.md | TODO |
| P6 | End-to-end orchestrator | Waniya | 12_pipeline_orchestrator | TODO |
| P7 | Gold validation (FK integrity, duplicates) | Waniya | 13_gold_validation | TODO |
| P8 | Audit/quarantine/intraday views for BI | Waniya | 14_bi_views | TODO |
| P9 | Power BI connection (token) + star-schema model view | Waniya | .pbix | TODO |
| P10 | Dashboards: 4 business pages + Pipeline Monitoring | Waniya | .pbix | TODO |
| P11 | Spark UI / query profile screenshot + explanation | Khushbakht | docs/screenshots/ | TODO |
| P12 | FinOps measurements and estimate | Khushbakht | REPORT.md section 7 | TODO |
| P13 | Architecture diagram | Khushbakht | docs/architecture.png | TODO |
| P14 | Report sections: 1,2,4,7 + engineering decisions (K); drift/PII/Silver decisions, 5, 6 (W) | Both | docs/REPORT.md | TODO |
| P15 | Optional prediction component (Q9, Q10) | Both | 15_prediction | Decide at check-in |
| P16 | README final + tagged release | Khushbakht | v1.0 tag | TODO |
| P17 | Final report PDF export | Waniya | docs/REPORT.pdf | TODO |

## Phase 3 Requirement Checklist
- [ ] Star schema: fact + dimension tables (not copies of Silver)
- [ ] Gold data dictionary with PK/FK relationships (ER diagram)
- [ ] OPTIMIZE / Liquid Clustering demonstrated
- [ ] Gold refreshes automatically after Silver (orchestrator)
- [ ] Gold runs logged with rows aggregated + execution time
- [ ] Power BI connected to Gold; relationships match the star schema
- [ ] Dashboard: at least 3 visuals + audit/error-log visuals
- [ ] PDF: architecture diagram, decision log, DAG analysis, FinOps
- [ ] GitHub repo, BI file/link, PDF submitted

## Phase 3 Risks
| Risk | Mitigation |
|---|---|
| Power BI file connects to one workspace only | Connect to Waniya's workspace; she pulls and runs 08-11 there |
| Classic Spark UI not available on serverless | Use Query Profile / df.explain("formatted") screenshots |
| Incremental file fully overlaps full load (inserted=0) | Show a Gold run with 0 changes plus a controlled test (modify a few Bronze rows) |
| Free Edition has no billing data | FinOps uses measured runtimes + stated pricing assumptions |
| Only ~31 days of data | Day-of-week and regime results are indicative; state this in the report |
| Power BI overruns | Khushbakht takes the Pipeline Monitoring page and DAX measures |
| Unequal workload | Rule 16 in TASK_DIVISION: rebalance at check-in |

## Milestones
| Milestone | Target | Status |
|---|---|---|
| Phase 1 complete | before 2026-10-10 | Done |
| Phase 2 complete (Bronze + Silver) | 2026-10-11 | Done |
| Gold built (08-11) + logged | <date> | |
| Orchestrator + validation (12-13) | <date> | |
| Power BI dashboard | <date> | |
| Report PDF + submission | <date> | |
