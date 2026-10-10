# Phase 2 Project Plan: Bronze & Silver Pipeline

**Project:** Cryptocurrency Market Analytics and Investment Decision Support
**Team:** Khushbakht (Member 1), Waniya (Member 2)
**Platform:** Databricks Free Edition, PySpark, Delta Lake
**Source:** Existing CoinGecko JSON files (manual ingestion approved by professor)
**Repo:** https://github.com/Waniya317/Cryptocurrency-Market-Analytics-and-Investment-Decision-Support

**Last updated:** 2026-10-11


## Goal
Build a Bronze and Silver pipeline that is idempotent, parameterized,
logged, and schema-safe.

## Architecture
Raw JSON (Volume) -> Bronze (Delta) -> Silver (Delta) -> [Gold: Phase 3] -> Power BI

## Environment
- Catalog: crypto | Schemas: bronze, silver, ops
- Volume: /Volumes/crypto/bronze/raw_files/ (both JSON files directly inside)
- Tables: crypto.bronze.market_data_raw, crypto.bronze.quarantine,
  crypto.silver.market_data_clean, crypto.ops.pipeline_execution_logs

## Phase 1 Recap (done)
- 94 valid coins from ~100 IDs
- Full load: 30 days hourly, 66,401 observations
- Incremental load: 7 days hourly, 14,474 observations
- Fields: coin ID, timestamp, price, market cap, total volume

## Phases
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
| H | Schema drift / quarantine (Silver side) | Waniya | 06_schema_drift_quarantine | DONE |
| I | Validation checks | Waniya | 07_validation_checks | DONE |
| J | Data model docs | Waniya | DATA_MODEL.md | DONE |
| K | README + final push | Khushbakht | README.md, tagged commit | TODO |
| L | Idempotency proof (Bronze) | Khushbakht | PIPELINE_RUN_LOG.md + screenshots | DONE |
| L2 | Idempotency proof (Silver) | Waniya | PIPELINE_RUN_LOG.md | DONE |
| M | Bronze notebooks pushed to GitHub | Khushbakht | src/pyspark/ 00-03 | DONE |
| N | All MD docs + screenshots uploaded to GitHub | Khushbakht | docs/ | IN PROGRESS |
| O | PR review: Bronze -> main | Waniya | Merged PR | DONE |


## Requirement Checklist

- [x] Databricks Free Edition used
- [x] All PySpark code for Bronze and Silver pipeline available in GitHub
- [x] Explicit StructType/StructField schemas used
- [x] Bronze and Silver columns, types, and keys documented in DATA_MODEL.md
- [x] load_timestamp included in Bronze and Silver schemas
- [x] Idempotent Bronze and Silver loads using Delta MERGE INTO
- [x] Parameterized backfill runner implemented
- [x] Schema drift handling and quarantine implemented
- [x] pipeline_execution_logs created and populated
- [ ] README updated with data models and execution instructions
- [x] Pipeline validation checks completed
- [x] Pipeline screenshots captured and uploaded

## Risks
| Risk | Mitigation |
|---|---|
| CoinGecko API blocked in Databricks | Manual JSON upload (approved) |
| Duplicate rows on re-run | MERGE INTO on (coin_id, ts_ms), update only if values changed |
| Schema changes in JSON | Records with different keys go to crypto.bronze.quarantine |
| Free Edition limits | Small data (~81k rows), avoid heavy jobs |
| Two separate workspaces | Same names, same notebooks via GitHub |
| %run fails when pasted as a comment | Keep %run alone in its own cell |
| Stale or conflicting docs | GitHub is the single source of truth, logs are append-only |


## Milestones

| Milestone | Target Date | Status |
|---|---|---|
| Setup + schemas + logging | 2026-10-10 | Done |
| Bronze done + pushed to GitHub | 2026-10-10 | Done |
| Silver transformation + idempotency proof | 2026-10-10 | Done |
| Backfill + schema drift + validation | 2026-10-10 | Done |
| Documentation + screenshots | 2026-10-11 | Done in Databricks; GitHub push to verify |
| README update + final push | Pending | TODO |

