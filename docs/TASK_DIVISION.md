# Task Division

**Member 1:** Khushbakht | **Member 2:** Waniya

==================== PHASE 2 (COMPLETE) ====================

## Phase 2 Split Rule
Khushbakht owns ingestion (Bronze) and setup.
Waniya owns transformation (Silver), quality, and data model docs.
Each person reviews the other's work before merging.

## Phase 2: FILES KHUSHBAKHT CREATED
| File | Location | Purpose | Status |
|---|---|---|---|
| 00_config_schemas | src/pyspark/ | Paths, StructType schemas | DONE, pushed |
| 01_logging_utils | src/pyspark/ | Log table, helpers, shared bronze_load() | DONE, pushed |
| 02_bronze_full_load | src/pyspark/ | Full load JSON -> Bronze (MERGE INTO) | DONE, pushed |
| 03_bronze_incremental | src/pyspark/ | Incremental JSON -> Bronze (MERGE INTO) | DONE, pushed |
| README.md | root | Data models + execution instructions | DONE (Phase 3 final version: P16) |
| PROJECT_PLAN.md | docs/ | Plan, phases, checklist, risks | DONE (kept updated) |
| TASK_DIVISION.md | docs/ | This file | DONE (kept updated) |
| WORKLOG.md | docs/logs/ | Daily work record | Ongoing |
| PIPELINE_RUN_LOG.md | docs/logs/ | Every run + idempotency proof | Ongoing |
| DECISIONS_LOG.md | docs/logs/ | Design decisions | Ongoing |

## Phase 2: FILES WANIYA CREATED
| File | Location | Purpose | Status |
|---|---|---|---|
| 04_silver_transform | src/pyspark/ | Clean, validate, dedupe -> Silver (MERGE INTO) | DONE, pushed |
| 05_backfill_runner | src/pyspark/ | Reprocess Bronze -> Silver by date range | DONE, pushed |
| 06_schema_drift_quarantine | src/pyspark/ | Quarantine records with unexpected/missing fields | DONE, pushed |
| 07_validation_checks | src/pyspark/ | Row counts, duplicates, nulls, reconciliation | DONE, pushed |
| DATA_MODEL.md | docs/ | Bronze + Silver columns, types, keys | DONE |
| ERROR_LOG.md | docs/logs/ | All errors and fixes | Ongoing |
| VISUALIZATION_LOG.md | docs/logs/ | Dashboard and visual tracking | Ongoing |

## Phase 2: Setup Tasks
| Task | Owner | Reviewer | Status |
|---|---|---|---|
| Databricks setup (catalog, schemas, Volume) | Khushbakht | Waniya | DONE |
| Git folder linked + Bronze notebooks pushed | Khushbakht | Waniya | DONE |
| All MD docs + screenshots uploaded to GitHub | Khushbakht | Waniya | DONE |
| Waniya clones repo + own workspace + JSON in her Volume | Waniya | Khushbakht | DONE |
| Idempotency proof for Bronze | Khushbakht | Waniya | DONE |
| Idempotency proof for Silver | Waniya | Khushbakht | DONE |

## Phase 2: Waniya Onboarding (kept for reference)
1. Pull or clone the repo (Databricks: Workspace -> Create -> Git folder -> repo URL, or git clone).
2. Read docs/PROJECT_PLAN.md, docs/TASK_DIVISION.md, and the logs in docs/logs/.
3. In her Databricks: create catalog crypto, schemas bronze/silver/ops, Volume
   crypto.bronze.raw_files, and upload both JSON files into it.
4. Run 00 and 01 from src/pyspark/ so the same 4 tables exist in her workspace.
5. Create branch feat/silver-waniya and start on 04_silver_transform.

## Phase 2: Shared Contract
- Bronze table: crypto.bronze.market_data_raw
- Silver table: crypto.silver.market_data_clean
- Quarantine table: crypto.bronze.quarantine
- Log table: crypto.ops.pipeline_execution_logs
- Business key: (coin_id, ts_ms) in Bronze, (coin_id, event_ts) in Silver
- Bronze columns: coin_id, ts_ms, price, market_cap, total_volume,
  source_file, load_type, batch_id, load_timestamp
- Reusable helpers in 01_logging_utils: new_batch_id(), merge_metrics(table),
  log_run(...), create_tables().
- Notebook header: "%run ./00_config_schemas" or "%run ./01_logging_utils"
  alone in its own first cell.

==================== PHASE 3 (IN PROGRESS) ====================

## Phase 3 Split Rule
Equal workload (about 15 hours each), notebooks in sequence.
Khushbakht = Gold build (08-11), data model doc, Spark DAG, FinOps, architecture.
Waniya = automation + quality (12-14), Power BI, dashboards, report export.
Each reviews the other's work before merging.

## Phase 3: FILES KHUSHBAKHT WILL CREATE
| File | Location | Purpose | Status |
|---|---|---|---|
| 00_config_schemas (patch) | src/pyspark/ | Gold table names (T_DIM_COIN ... T_FACT_PORTF) | DONE |
| 01_logging_utils (patch) | src/pyspark/ | gold_merge / run_gold_merge helpers | DONE |
| 08_gold_setup | src/pyspark/ | Explicit DDL for all Gold tables, liquid clustering, informational PK/FK | DONE |
| 09_gold_dimensions | src/pyspark/ | dim_coin, dim_date, dim_hour, dim_scenario, bridge_scenario_coin | DONE |
| 10_gold_facts | src/pyspark/ | fact_market_hourly, fact_coin_daily, fact_portfolio_daily (MERGE + logging) | DONE |
| 11_gold_optimize | src/pyspark/ | OPTIMIZE + before/after proof | DONE |
| GOLD_DATA_MODEL.md | docs/ | ER diagram + data dictionary + business question mapping | DONE |
| optimize_before_after.png | docs/screenshots/ | OPTIMIZE evidence | DONE |
| Query Profile screenshot | docs/screenshots/ | DAG of the fact_coin_daily aggregation | IN PROGRESS (explain plan captured) |
| architecture.png | docs/ | Flow diagram for the report | TODO |
| REPORT.md sections 1, 2, 3 (engineering decisions), 4, 7 | docs/ | Architecture, model, decisions, DAG, FinOps | IN PROGRESS |
| README.md (Phase 3 section) + v1.0 tag | root | Run instructions, release | Section DONE, tag TODO |

## Phase 3: FILES WANIYA WILL CREATE
| File | Location | Purpose | Status |
|---|---|---|---|
| Phase 2 fixes (price rule, R006/R007 counts, screenshot names) | docs/ | Docs match code | TODO |
| Pull main, apply 00/01 patches, run 08-11 in her workspace | Databricks | Gold tables exist where Power BI connects | TODO |
| 12_pipeline_orchestrator | src/pyspark/ | Runs 03 -> 04 -> 09 -> 10 in one go, logs the run | TODO |
| 13_gold_validation | src/pyspark/ | FK integrity, duplicates, count reconciliation | TODO |
| 14_bi_views | src/pyspark/ | Audit, quarantine, intraday-vs-historical views for Power BI | TODO |
| Crypto_Dashboard.pbix | bi/ | Power BI model + 4 business pages + Pipeline Monitoring | TODO |
| REPORT.md sections 3 (drift, PII, Silver decisions), 5, 6 | docs/ | Decisions, dashboard, validation | TODO |
| REPORT.pdf | docs/ | Final export for submission | TODO |

## Optional (decide at check-in): prediction component (Q9, Q10)
15_prediction (UP/DOWN model, writes crypto.gold.fact_prediction). If built:
Khushbakht = features + training, Waniya = dashboard page.

## Phase 3: Dependencies
- 08 -> 09 and 10 -> 11 (same owner, run in order).
- 12 needs 09 and 10. 13 needs 09 and 10. 14 needs 10.
- Power BI connects to Waniya's workspace (direct, with token). Khushbakht's 08-11
  notebooks reach it through GitHub; Waniya pulls and runs them there.
- While waiting, Waniya does the Phase 2 fixes and tests the Power BI connection.
- If Power BI overruns, Khushbakht builds the Pipeline Monitoring page and DAX measures.

## Phase 3: Shared Contract
- Gold schema: crypto.gold
- Tables: dim_coin, dim_date, dim_hour, dim_scenario, bridge_scenario_coin,
  fact_market_hourly, fact_coin_daily, fact_portfolio_daily
- coin_key = xxhash64(coin_id), date_key = yyyymmdd INT, hour_key = 0-23 INT,
  scenario_key = xxhash64(scenario_name)
- Helpers in 01_logging_utils: gold_merge(), run_gold_merge() (logs layer "gold")
- Log layer names: "gold", "orchestrator", "validation"
- Every Gold run logs rows read/written and execution time to pipeline_execution_logs.

## Working Rules (apply to both phases)
1. One branch per task (feat/bronze-khushbakht, feat/silver-waniya, feat/gold-khushbakht, feat/bi-waniya), merge to main via PR.
2. Commit messages: feat(bronze): ..., fix(silver): ..., docs: ...
3. Every run goes in logs/PIPELINE_RUN_LOG.md.
4. Every bug goes in logs/ERROR_LOG.md.
5. Every work session goes in logs/WORKLOG.md (name in Person column).
6. Any schema change must be noted in the data model docs and DECISIONS_LOG.md.
7. Do not edit the other person's file without telling them. Use a PR comment.
8. Both members may append rows to any log file. Owner only means who maintains the file.
9. Databricks does not auto-push: use the Git button -> Commit & Push after every task.
10. ALL MD files live in GitHub. GitHub is the single source of truth.
11. Before editing any file: pull the latest. After editing: commit and push right away.
12. Log files are append-only: add new rows at the bottom, never rewrite old rows.
13. Each person updates their own docs and logs after every work session.
14. Screenshots go in docs/screenshots/ with clear names.
15. Record the runtime of every Gold and orchestrator run (needed for FinOps).
16. If the workload feels unfair, say so in WORKLOG.md or at the check-in and rebalance.

## Sync
Check-in: <day/time>. Blockers go in WORKLOG.md.