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

## Phase 3 Runs (times in the logs table are UTC; Pakistan time = UTC+5)
Rows In = rows_aggregated (rows in the MERGE source). Duration = end_time - start_time from the logs table.
| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Duration (s) | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| R008 | 2026-10-17 | Khushbakht | gold | 08_gold_setup: 8 tables created | n/a | n/a | n/a | <fill> | SUCCESS | Liquid clustering on the 3 facts (verified: hourly and daily by coin_key, date_key; portfolio by date_key) |
| R009 | 2026-10-17 | Khushbakht | gold | 09: dim_coin | 94 | 94 | 0 | <fill> | SUCCESS | 94 coins |
| R010 | 2026-10-17 | Khushbakht | gold | 09: dim_date | 31 | 31 | 0 | <fill> | SUCCESS | 31 calendar days |
| R011 | 2026-10-17 | Khushbakht | gold | 09: dim_hour | 24 | 24 | 0 | <fill> | SUCCESS | |
| R012 | 2026-10-17 | Khushbakht | gold | 09: dim_scenario | 5 | 5 | 0 | 6.3 | SUCCESS | run_20261017_073607_ad72ab |
| R013 | 2026-10-17 | Khushbakht | gold | 09: bridge_scenario_coin | 282 | 282 | 0 | 9.3 | SUCCESS | 94 + 2 + 5 + 94 + 87 coin weights across 5 scenarios |
| R014 | 2026-10-17 | Khushbakht | gold | 10: fact_market_hourly | 66401 | 66401 | 0 | 7.2 | SUCCESS | Silver rows read: 66401; run_20261017_074039_b80855 |
| R015 | 2026-10-17 | Khushbakht | gold | 10: fact_coin_daily | 2914 | 2914 | 0 | 6.3 | SUCCESS | 94 coins x 31 days; run_20261017_074051_fd9a77 |
| R016 | 2026-10-17 | Khushbakht | gold | 10: fact_portfolio_daily | 155 | 155 | 0 | 6.3 | SUCCESS | 5 scenarios x 31 days; run_20261017_074155_2ac6f5 |
| R017 | 2026-10-17 | Khushbakht | gold | 10 re-run: fact_coin_daily | 2914 | 0 | 0 | 7.4 (printed) | SUCCESS | Idempotency proof; fact_market_hourly and fact_portfolio_daily re-run: <confirm 0 / 0> |
| R018 | 2026-10-17 | Khushbakht | gold | 11: OPTIMIZE on the 3 facts | n/a | n/a | n/a | <fill> | SUCCESS | fact_market_hourly 2 -> 1 files (3,537,209 -> 3,525,131 bytes); fact_coin_daily and fact_portfolio_daily already 1 file |
| R019 | | Waniya | orchestrator | 12: typical incremental run | | | | | PLANNED | FinOps measurement |
| R020 | | Waniya | orchestrator | 12 (re-run) | | 0 | 0 | | PLANNED | Idempotency proof |
| R021 | | Waniya | orchestrator | 12 demo: controlled change of 5 Bronze rows | | | | | PLANNED | Shows Silver and Gold updated > 0 |
| R022 | | Waniya | validation | 13_gold_validation | | | | | PLANNED | FK, duplicates, reconciliation |

Query to fill the remaining <fill> cells (run in Databricks):
SELECT run_id, file_or_params, rows_inserted, rows_updated,
       round((unix_millis(end_time) - unix_millis(start_time)) / 1000.0, 1) AS duration_s, status
FROM crypto.ops.pipeline_execution_logs
WHERE layer IN ('gold', 'orchestrator', 'validation')
ORDER BY start_time;
Rows read ("rows_aggregated") is written inside the file_or_params text of each row.

## Phase 3 Idempotency Proof
| Test | Run 1 inserted/updated | Run 2 inserted/updated | Duplicate keys? | Result |
|---|---|---|---|---|
| Re-run Gold fact_coin_daily (10) | 2914 / 0 | 0 / 0 | checked in 13_gold_validation | PASS |
| Re-run Gold fact_market_hourly (10) | 66401 / 0 | <confirm 0 / 0> | checked in 13_gold_validation | |
| Re-run Gold fact_portfolio_daily (10) | 155 / 0 | <confirm 0 / 0> | checked in 13_gold_validation | |
| Re-run Gold dimensions (09) | 94+31+24+5+282 inserted | <confirm 0 / 0> | checked in 13_gold_validation | |
| Re-run orchestrator (12) | | 0 / 0 | | |

## Final Gold Counts
| Table | Rows |
|---|---|
| dim_coin | 94 |
| dim_date | 31 |
| dim_hour | 24 |
| dim_scenario | 5 |
| bridge_scenario_coin | 282 |
| fact_market_hourly | 66401 |
| fact_coin_daily | 2914 |
| fact_portfolio_daily | 155 |

## OPTIMIZE Results (11_gold_optimize)
| Table | Clustering | Files before -> after | Bytes before -> after |
|---|---|---|---|
| crypto.gold.fact_market_hourly | coin_key, date_key | 2 -> 1 | 3,537,209 -> 3,525,131 |
| crypto.gold.fact_coin_daily | coin_key, date_key | 1 -> 1 | 229,985 -> 229,985 |
| crypto.gold.fact_portfolio_daily | date_key | 1 -> 1 | 3,726 -> 3,726 |
Query time before/after (fact_market_hourly, one coin, last 7 days): <fill from the query_s columns>.
The data is small, so only fact_market_hourly had more than one file to compact.

## Phase 3 Screenshots (docs/screenshots/)
| File | Shows |
|---|---|
| gold_tables.png | SHOW TABLES IN crypto.gold (8 tables) and clustering columns |
| gold_facts_first_run.png | 10 output: fact_coin_daily rows_in_source=2914 inserted=2914 updated=0 |
| gold_facts_rerun_zero.png | 10 re-run: fact_coin_daily inserted=0 updated=0 |
| gold_execution_logs.png | gold rows in pipeline_execution_logs with rows_aggregated |
| optimize_before_after.png | OPTIMIZE table: files and bytes before/after |
| spark_dag_fact_coin_daily.png | Query Profile / DAG of the fact_coin_daily aggregation |
| orchestrator_run.png | 12 output with all layers |
| gold_validation.png | 13 output, all checks PASS |
| powerbi_model_view.png | One-to-many relationships |
| dashboard_*.png | One screenshot per dashboard page |

## FinOps Measurements (copy from the logs table)
| Run | Duration (s) | Rows read | Rows written |
|---|---|---|---|
| Gold facts only (10), first load | 19.8 (7.2 + 6.3 + 6.3, merge time only) | 66401 | 69470 (66401 + 2914 + 155) |
| Gold facts only (10), re-run | <fill> | 66401 | 0 |
| Orchestrator, typical incremental | | | |
