# Cryptocurrency Market Analytics and Investment Decision Support

Databricks + PySpark + Delta Lake + Power BI pipeline over CoinGecko hourly data (94 coins).

**Team:** Khushbakht (Bronze, Gold build, FinOps), Waniya (Silver, orchestration, validation, Power BI)

## Architecture
Raw JSON (Unity Catalog Volume) -> Bronze -> Silver -> Gold (star schema) -> Power BI

## Repo layout
| Path | Content |
|---|---|
| src/ | Phase 1 Python scripts (get_full_load.py, get_incremental_load.py) |
| src/pyspark/ | Databricks notebooks 00-14 |
| data/raw/ | Source JSON files |
| bi/ | Power BI file (Crypto_Dashboard.pbix) |
| docs/ | PROJECT_PLAN.md, TASK_DIVISION.md, DATA_MODEL.md, GOLD_DATA_MODEL.md, REPORT.md / REPORT.pdf |
| docs/logs/ | WORKLOG, ERROR_LOG, PIPELINE_RUN_LOG, VISUALIZATION_LOG, DECISIONS_LOG |
| docs/screenshots/ | Run proof, Spark DAG, dashboard screenshots |

## Setup
1. Databricks Free Edition: create catalog `crypto` with schemas bronze, silver, gold, ops.
2. Create Volume crypto.bronze.raw_files and upload both JSON files from data/raw/ directly into it.
3. Workspace -> Create -> Git folder -> paste this repo URL.

## Run order
Phase 2 (Bronze and Silver)
1. 01_logging_utils (runs 00 via %run, creates the Delta tables)
2. 02_bronze_full_load
3. 03_bronze_incremental
4. 04_silver_transform
5. 05_backfill_runner
6. 06_schema_drift_quarantine
7. 07_validation_checks

Phase 3 (Gold and BI)
8. 08_gold_setup
9. 09_gold_dimensions
10. 10_gold_facts
11. 11_gold_optimize
12. 12_pipeline_orchestrator (end-to-end: 03 -> 04 -> 09 -> 10, logged)
13. 13_gold_validation
14. 14_bi_views

Each notebook starts with a %run line alone in its own cell.
Parameters: widgets `path` and `batch_id` on 02 and 03; start_date / end_date on 05.
Re-running any notebook is safe (MERGE INTO): repeats show inserted=0 updated=0.
To process a new incremental file end to end, run only 12_pipeline_orchestrator.

## Power BI
1. Databricks: SQL Warehouses -> your warehouse -> Connection details (Server hostname, HTTP path).
2. Create a personal access token (never commit it to GitHub).
3. Power BI Desktop -> Get Data -> Databricks -> enter hostname and HTTP path -> use the token.
4. Load the crypto.gold tables and the views from 14_bi_views, then check Model view:
   one-to-many relationships from each dimension to the facts (see docs/GOLD_DATA_MODEL.md).

## Data models
Bronze/Silver: docs/DATA_MODEL.md. Gold: docs/GOLD_DATA_MODEL.md.
Run history: docs/logs/PIPELINE_RUN_LOG.md and the table crypto.ops.pipeline_execution_logs.
Final report: docs/REPORT.pdf.

## Git workflow
Branch per task, PR into main, commit after every task, docs live in GitHub.
Full rules in docs/TASK_DIVISION.md.
