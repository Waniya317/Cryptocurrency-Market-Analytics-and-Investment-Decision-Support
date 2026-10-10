# Pipeline Run Log

Run IDs match the run_id column in crypto.ops.pipeline_execution_logs.
Append new rows at the bottom. Do not rewrite old rows.

| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| R001 | 2026-10-10 | Khushbakht | bronze | 02: crypto_hourly_full_load_100coins.json | 66401 | 66401 | 0 | SUCCESS | First full load, quarantined=0 |
| R002 | 2026-10-10 | Khushbakht | bronze | 03: crypto_hourly_incremental_load_94coins.json | 14474 | 0 | 0 | SUCCESS | All rows already in full load (7 days overlap 30 days), no changes |
| R003 | 2026-10-10 | Khushbakht | bronze | 02 re-run (same file) | 66401 | 0 | 0 | SUCCESS | Idempotency proof |
| R004 | 2026-10-10 | Waniya | silver | 04: Bronze to Silver transformation | 66401 | 66401 | 0 | SUCCESS | Initial Silver transformation; 66401 rows inserted |
| R005 | 2026-10-10 | Waniya | silver | 04: Bronze to Silver transformation (re-run) | 66401 | 0 | 0 | SUCCESS | Re-run completed with no new inserts or updates |
| R006 | 2026-10-10 | Waniya | backfill | 05: start_date=2026-09-04, end_date=2026-10-04 | 66401 (current date-range count; not run input) | 0 | 0 | SUCCESS | Current Silver date-range count=66401 across 94 coins; actual run input count not recorded |
| R007 | 2026-10-10 | Waniya | schema_drift | 06: crypto_hourly_full_load_100coins.json | Unknown | 0 | 0 | SUCCESS | Schema-drift check succeeded; inspected-row count not recorded |
## Idempotency Proof
| Test | Run 1 inserted/updated | Run 2 inserted/updated | Duplicate keys? | Result |
|---|---|---|---|---|
| Re-run bronze full load | 66401 / 0 | 0 / 0 | 0 rows | PASS |
| Incremental load over existing data | 0 / 0 | 0 / 0 | 0 rows | PASS |
| Re-run silver | 66401 / 0 | 0 / 0 | 0 rows | PASS |

## Final Bronze Counts
| Check | Value |
|---|---|
| Total rows in market_data_raw | 66401 |
| Distinct coins | 94 |
| Rows in quarantine | 0 |

## Final Silver Counts
| Check | Value |
|---|---|
| Total rows in market_data_clean (Silver) | 66401 |
| Silver validation checks | PASS |
| Silver duplicate keys | 0 |
| Rows in quarantine | 0 |

## Screenshots (docs/screenshots/)
| File | Shows |
|---|---|
| bronze_full_run.png | 02 output: read=66401 good=66401 quarantined=0 inserted=66401 updated=0 |
| bronze_incremental_run.png | 03 output: read=14474 good=14474 quarantined=0 inserted=0 updated=0 |
| execution_logs_table.png | crypto.ops.pipeline_execution_logs with both runs |
| silver_transform.png | 04 output: initial Silver load inserted=66401, updated=0, and idempotency rerun inserted=0 |
| backfill_runner.png | Backfill execution output for date range 2026-09-04 to 2026-10-04 |
| schma_drift.png | 06 output: schema drift check output with 0 quarantined rows |
| valdation_checks.png | Validation checks output cell showing PASS status and duplicates=0 |
