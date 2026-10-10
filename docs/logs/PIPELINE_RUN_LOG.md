# Pipeline Run Log

Run IDs match the run_id column in crypto.ops.pipeline_execution_logs.
Append new rows at the bottom. Do not rewrite old rows.

| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| R001 | 2026-10-10 | Khushbakht | bronze | 02: crypto_hourly_full_load_100coins.json | <fill> | <fill> | 0 | SUCCESS | First full load, quarantined=<fill> |
| R002 | 2026-10-10 | Khushbakht | bronze | 03: crypto_hourly_incremental_load_94coins.json | <fill> | <fill> | <fill> | SUCCESS | First incremental load |
| R003 | 2026-10-10 | Khushbakht | bronze | 03 re-run (same file) | <fill> | 0 | 0 | SUCCESS | Idempotency proof |
| R004 | 2026-10-10 | Khushbakht | bronze | 02 re-run (same file) | <fill> | 0 | 0 | SUCCESS | Idempotency proof |

## Idempotency Proof
| Test | Run 1 inserted/updated | Run 2 inserted/updated | Duplicate keys? | Result |
|---|---|---|---|---|
| Re-run bronze full load | <fill> / 0 | 0 / 0 | 0 rows | PASS |
| Re-run bronze incremental | <fill> / <fill> | 0 / 0 | 0 rows | PASS |
| Re-run silver (Waniya) | | | | |

## Final Bronze Counts
| Check | Value |
|---|---|
| Total rows in market_data_raw | <fill> |
| Distinct coins | <fill> |
| Rows in quarantine | <fill> |

## Screenshots (docs/screenshots/)
| File | Shows |
|---|---|
| bronze_full_run.png | 02 output line |
| bronze_incremental_run.png | 03 output line |
| bronze_rerun_zero.png | Re-run with inserted=0 updated=0 |
| execution_logs_table.png | crypto.ops.pipeline_execution_logs |
