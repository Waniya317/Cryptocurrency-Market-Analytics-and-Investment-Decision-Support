# Pipeline Run Log

Run IDs match the run_id column in crypto.ops.pipeline_execution_logs.
Append new rows at the bottom. Do not rewrite old rows.

## Phase 2 Runs
| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| R001 | 2026-10-10 | Khushbakht | bronze | 02: crypto_hourly_full_load_100coins.json | 66401 | 66401 | 0 | SUCCESS | First full load, quarantined=0 |
| R002 | 2026-10-10 | Khushbakht | bronze | 03: crypto_hourly_incremental_load_94coins.json | 14474 | 0 | 0 | SUCCESS | All rows already in full load (7 days overlap 30 days), no changes |
| R003 | 2026-10-10 | Khushbakht | bronze | 02 re-run (same file) | 66401 | 0 | 0 | SUCCESS | Idempotency proof |
| R004 | 2026-10-10 | Waniya | silver | 04: Bronze to Silver transformation | 66401 | 66401 | 0 | SUCCESS | Initial Silver transformation; 66401 rows inserted |
| R005 | 2026-10-10 | Waniya | silver | 04: Bronze to Silver transformation (re-run) | 66401 | 0 | 0 | SUCCESS | Re-run completed with no new inserts or updates |
| R006 | 2026-10-10 | Waniya | backfill | 05: start_date=2026-09-04, end_date=2026-10-04 | 66401 (current date-range count; not run input) | 0 | 0 | SUCCESS | Current Silver date-range count=66401 across 94 coins; actual run input count not recorded (see E005) |
| R007 | 2026-10-10 | Waniya | schema_drift | 06: crypto_hourly_full_load_100coins.json | Unknown | 0 | 0 | SUCCESS | Schema-drift check succeeded; inspected-row count not recorded (see E005) |

## Phase 2 Idempotency Proof
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

## Phase 2 Screenshots (docs/)
| File | Shows |
|---|---|
| Screenshot 2026-10-10 185111.png, 185649.png, 185902.png, 185954.png | Bronze proof: 02 output (read=66401 inserted=66401), 03 output (read=14474 inserted=0), execution logs table, re-run |
| silver_transform_ss1.png | 04 output: initial Silver load inserted=66401, updated=0, and idempotency re-run inserted=0 |
| backfill_runner_ss1.png | Backfill output for 2026-09-04 to 2026-10-04 |
| schema_drift_ss1.png | 06 output: schema drift check with 0 quarantined rows |
| validation_checks_ss1.png | Validation checks output: PASS status and duplicates=0 |

## Phase 3 Runs (Run ID = run_id in the logs table; fill the <fill> cells with the query at the end of this section)
| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Duration (s) | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| R008 | 2026-10-17 | Khushbakht | gold | 08_gold_setup: 8 tables created | n/a | n/a | n/a | <fill> | SUCCESS | Liquid clustering on the 3 facts |
| R009 | 2026-10-17 | Khushbakht | gold | 09: dim_coin | <fill> | <fill> | 0 | <fill> | SUCCESS | First load, 94 coins expected |
| R010 | 2026-10-17 | Khushbakht | gold | 09: dim_date | <fill> | <fill> | 0 | <fill> | SUCCESS | Calendar days between first and last Silver date |
| R011 | 2026-10-17 | Khushbakht | gold | 09: dim_hour | 24 | 24 | 0 | <fill> | SUCCESS | |
| R012 | 2026-10-17 | Khushbakht | gold | 09: dim_scenario | 5 | 5 | 0 | <fill> | SUCCESS | |
| R013 | 2026-10-17 | Khushbakht | gold | 09: bridge_scenario_coin | <fill> | <fill> | 0 | <fill> | SUCCESS | Weights sum to 1 per scenario |
| R014 | 2026-10-17 | Khushbakht | gold | 10: fact_market_hourly | <fill> | <fill> | 0 | <fill> | SUCCESS | Silver rows read: 66401 |
| R015 | 2026-10-17 | Khushbakht | gold | 10: fact_coin_daily | <fill> | <fill> | 0 | <fill> | SUCCESS | |
| R016 | 2026-10-17 | Khushbakht | gold | 10: fact_portfolio_daily | <fill> | <fill> | 0 | <fill> | SUCCESS | |
| R017 | 2026-10-17 | Khushbakht | gold | 10 re-run (3 facts) | <fill> | 0 | 0 | <fill> | <fill> | Idempotency proof; fill after confirming 0 / 0 |
| R018 | 2026-10-17 | Khushbakht | gold | 11: OPTIMIZE on the 3 facts | n/a | n/a | n/a | <fill> | SUCCESS | Files before -> after in optimize_before_after.png |
| R019 | | Waniya | orchestrator | 12: typical incremental run | | | | | PLANNED | FinOps measurement |
| R020 | | Waniya | orchestrator | 12 (re-run) | | 0 | 0 | | PLANNED | Idempotency proof |
| R021 | | Waniya | orchestrator | 12 demo: controlled change of 5 Bronze rows | | | | | PLANNED | Shows Silver and Gold updated > 0 |
| R022 | | Waniya | validation | 13_gold_validation | | | | | PLANNED | FK, duplicates, reconciliation |

Query to fill the numbers (run in Databricks):
SELECT run_id, file_or_params, rows_inserted, rows_updated,
       round((unix_millis(end_time) - unix_millis(start_time)) / 1000.0, 1) AS duration_s, status
FROM crypto.ops.pipeline_execution_logs
WHERE layer IN ('gold', 'orchestrator', 'validation')
ORDER BY start_time;
"rows_aggregated" (rows read) is written inside the file_or_params text of each row.

## Phase 3 Idempotency Proof
| Test | Run 1 inserted/updated | Run 2 inserted/updated | Duplicate keys? | Result |
|---|---|---|---|---|
| Re-run Gold dimensions (09) | <fill> | 0 / 0 | | <fill> |
| Re-run Gold facts (10) | <fill> | 0 / 0 | | <fill> |
| Re-run orchestrator (12) | | 0 / 0 | | |

## Final Gold Counts
| Table | Rows |
|---|---|
| dim_coin | <fill> |
| dim_date | <fill> |
| dim_hour | 24 |
| dim_scenario | 5 |
| bridge_scenario_coin | <fill> |
| fact_market_hourly | <fill> |
| fact_coin_daily | <fill> |
| fact_portfolio_daily | <fill> |

## Phase 3 Screenshots (docs/screenshots/)
| File | Shows |
|---|---|
| gold_tables.png | SHOW TABLES IN crypto.gold |
| optimize_before_after.png | File count and query time before and after OPTIMIZE |
| spark_dag_fact_coin_daily.png | Query Profile / DAG of the fact_coin_daily aggregation |
| orchestrator_run.png | 12 output with all layers |
| gold_validation.png | 13 output, all checks PASS |
| powerbi_model_view.png | One-to-many relationships |
| dashboard_*.png | One screenshot per dashboard page |

## FinOps Measurements (copy from the logs table)
| Run | Duration (s) | Rows read | Rows written |
|---|---|---|---|
| Orchestrator, typical incremental | | | |
| Gold facts only (10) | <fill> | 66401 | <fill> |