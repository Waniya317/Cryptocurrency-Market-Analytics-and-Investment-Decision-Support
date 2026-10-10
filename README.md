# Cryptocurrency Market Analytics and Investment Decision Support

Databricks + PySpark + Delta Lake pipeline over CoinGecko hourly data (94 coins).

**Team:** Khushbakht (Bronze, setup, logging), Waniya (Silver, validation, data model)

## Architecture
Raw JSON (Unity Catalog Volume) -> Bronze -> Silver -> Gold (Phase 3) -> Power BI

## Repo layout
| Path | Content |
|---|---|
| src/ | Phase 1 Python scripts (get_full_load.py, get_incremental_load.py) |
| src/pyspark/ | Databricks notebooks 00-07 |
| data/raw/ | Source JSON files |
| docs/ | PROJECT_PLAN.md, TASK_DIVISION.md, DATA_MODEL.md |
| docs/logs/ | WORKLOG, ERROR_LOG, PIPELINE_RUN_LOG, VISUALIZATION_LOG, DECISIONS_LOG |
| docs/screenshots/ | Run proof |

## Setup
1. Databricks Free Edition: create catalog `crypto` with schemas bronze, silver, ops.
2. Create Volume crypto.bronze.raw_files and upload both JSON files from data/raw/ directly into it.
3. Workspace -> Create -> Git folder -> paste this repo URL.

## Run order
1. 01_logging_utils (runs 00 via %run, creates the 4 Delta tables)
2. 02_bronze_full_load
3. 03_bronze_incremental
4. 04_silver_transform (Waniya)
5. 05_backfill_runner, 06_schema_drift_quarantine, 07_validation_checks (Waniya)

Each notebook starts with a %run line alone in its own cell.
Parameters: widgets `path` and `batch_id` on 02 and 03.
Re-running any notebook is safe (MERGE INTO): repeats show inserted=0 updated=0.

## Data models
See docs/DATA_MODEL.md. Run history is in docs/logs/PIPELINE_RUN_LOG.md and in the
table crypto.ops.pipeline_execution_logs.

## Git workflow
Branch per task, PR into main, commit after every task, docs live in GitHub.
Full rules in docs/TASK_DIVISION.md.
