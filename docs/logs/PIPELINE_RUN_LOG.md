# Pipeline Run Log

Run IDs match the run_id column in crypto.ops.pipeline_execution_logs.
Append new rows at the bottom. Do not rewrite old rows.

| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| R001 | 2026-10-10 | Khushbakht | bronze | 02: crypto_hourly_full_load_100coins.json | 66401 | 66401 | 0 | SUCCESS | First full load, quarantined=0 |
| R002 | 2026-10-10 | Khushbakht | bronze | 03: crypto_hourly_incremental_load_94coins.json | 14474 | 0 | 0 | SUCCESS | All rows already in full load (7 days overlap 30 days), no changes |
| R003 | 2026-10-10 | Khushbakht | bronze | 02 re-run (same file) | 66401 | 0 | 0 | SUCCESS | Idempotency proof |

## Idempotency Proof
| Test | Run 1 inserted/updated | Run 2 inserted/updated | Duplicate keys? | Result |
|---|---|---|---|---|
| Re-run bronze full load | 66401 / 0 | 0 / 0 | 0 rows | PASS |
| Incremental load over existing data | 0 / 0 | 0 / 0 | 0 rows | PASS |
| Re-run silver (Waniya) | | | | |

## Final Bronze Counts
| Check | Value |
|---|---|
| Total rows in market_data_raw | 66401 |
| Distinct coins | 94 |
| Rows in quarantine | 0 |

## Screenshots (docs/screenshots/)
| File | Shows |
|---|---|
| bronze_full_run.png | 02 output: read=66401 good=66401 quarantined=0 inserted=66401 updated=0 |
| bronze_incremental_run.png | 03 output: read=14474 good=14474 quarantined=0 inserted=0 updated=0 |
| execution_logs_table.png | crypto.ops.pipeline_execution_logs with both runs |
