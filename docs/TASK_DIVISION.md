# Task Division

**Member 1:** Khushbakht
**Member 2:** Waniya

## Split Rule
Khushbakht owns ingestion (Bronze) and setup.
Waniya owns transformation (Silver), quality, and data model docs.
Each person reviews the other's work before merging.

## FILES KHUSHBAKHT WILL CREATE
| File | Location | Purpose | Status |
|---|---|---|---|
| 00_config_schemas | src/pyspark/ | Paths, StructType schemas | DONE, pushed |
| 01_logging_utils | src/pyspark/ | Log table, helpers, shared bronze_load() | DONE, pushed |
| 02_bronze_full_load | src/pyspark/ | Full load JSON -> Bronze (MERGE INTO) | DONE, pushed |
| 03_bronze_incremental | src/pyspark/ | Incremental JSON -> Bronze (MERGE INTO) | DONE, pushed |
| README.md | root | Data models + execution instructions | TODO (end) |
| PROJECT_PLAN.md | docs/ | Plan, phases, checklist, risks | DONE |
| TASK_DIVISION.md | docs/ | This file | DONE |
| WORKLOG.md | docs/logs/ | Daily work record | In progress |
| PIPELINE_RUN_LOG.md | docs/logs/ | Every run + idempotency proof | In progress |
| DECISIONS_LOG.md | docs/logs/ | Design decisions | In progress |

## FILES WANIYA WILL CREATE

| File | Location | Purpose | Status |
|---|---|---|---|
| 04_silver_transform | src/pyspark/ | Clean, validate, dedupe -> Silver (MERGE INTO) | DONE |
| 05_backfill_runner | src/pyspark/ | Runs backfill by date range | DONE |
| 06_schema_drift_quarantine | src/pyspark/ | Schema-drift detection and quarantine handling | DONE |
| 07_validation_checks | src/pyspark/ | Row counts, duplicates, nulls, reconciliation | DONE |
| DATA_MODEL.md | docs/ | Bronze + Silver columns, types, keys | DONE |
| ERROR_LOG.md | docs/logs/ | All errors and fixes | DONE |
| VISUALIZATION_LOG.md | docs/logs/ | Dashboard and visual tracking | UPDATED |

## Setup Tasks
| Task | Owner | Reviewer | Status |
|---|---|---|---|
| Databricks setup (catalog, schemas, Volume) | Khushbakht | Waniya | DONE |
| Git folder linked + Bronze notebooks pushed | Khushbakht | Waniya | DONE |
| All MD docs + screenshots uploaded to GitHub | Khushbakht | Waniya | VERIFY FINAL PUSH |
| Waniya clones repo + sets up her own workspace + uploads JSON to her Volume | Waniya | Khushbakht | DONE |
| Idempotency proof for Bronze | Khushbakht | Waniya | DONE |
| Idempotency proof for Silver | Waniya | Khushbakht | DONE |



## Waniya Onboarding

1. Cloned the repository and set up the Databricks workspace.
2. Reviewed the project plan, task division, and documentation logs.
3. Created the required catalog, schemas, Volume, and uploaded both JSON files.
4. Ran the configuration and logging notebooks.
5. Created and ran the Silver, backfill, schema-drift, and validation notebooks.

## Phase 3 Preview (proposed)
| Task | Owner |
|---|---|
| Gold dimensional model + risk/performance metrics | Khushbakht |
| Power BI dashboards (4) | Waniya |
| Optional UP/DOWN prediction model | Both |

## Shared Contract (Waniya codes Silver against this)
- Bronze table: crypto.bronze.market_data_raw
- Silver table: crypto.silver.market_data_clean
- Quarantine table: crypto.bronze.quarantine
- Log table: crypto.ops.pipeline_execution_logs
- Business key: (coin_id, ts_ms) in Bronze, (coin_id, event_ts) in Silver
- Bronze columns: coin_id, ts_ms, price, market_cap, total_volume,
  source_file, load_type, batch_id, load_timestamp
- Reusable helpers in 01_logging_utils: new_batch_id(), merge_metrics(table),
  log_run(...), create_tables(). Call these in 04-07 instead of rewriting them.
- Notebook header: "%run ./00_config_schemas" or "%run ./01_logging_utils"
  alone in its own first cell.

## Working Rules
1. One branch per task (feat/bronze-khushbakht, feat/silver-waniya), merge to main via PR.
2. Commit messages: feat(bronze): ..., fix(silver): ..., docs: ...
3. Every run goes in logs/PIPELINE_RUN_LOG.md.
4. Every bug goes in logs/ERROR_LOG.md.
5. Every work session goes in logs/WORKLOG.md (name in Person column).
6. Any schema change must be noted in DATA_MODEL.md and DECISIONS_LOG.md.
7. Do not edit the other person's file without telling them. Use a PR comment.
8. Both members may append rows to any log file. Owner only means who maintains the file.
9. Databricks does not auto-push: use the Git button -> Commit & Push after every task.
10. ALL MD files live in GitHub (docs/, docs/logs/, root README). GitHub is the
    single source of truth. Never keep a newer copy only on your laptop or in chat.
11. Before editing any file: pull the latest. After editing: commit and push right away
    with a "docs: ..." message.
12. Log files are append-only: add new rows at the bottom, never rewrite old rows. This
    avoids merge conflicts when both of us edit the same file.
13. Each person updates their own docs and logs in GitHub after every work session,
    so the other can check out the latest state at any time.
14. Screenshots go in docs/screenshots/ with clear names (e.g. silver_run_1.png).

## Sync
Check-in: <day/time>. Blockers go in WORKLOG.md.
