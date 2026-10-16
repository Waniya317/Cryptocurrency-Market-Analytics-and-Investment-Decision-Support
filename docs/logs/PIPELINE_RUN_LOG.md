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

## Phase 3 Runs (fill as you run; Run ID = run_id in the logs table)
| Run ID | Date | Run By | Layer | Parameters / File | Rows In | Inserted | Updated | Duration (s) | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| R008 | | Khushbakht | gold | 08_gold_setup | | | | | PLANNED | Tables created |
| R009 | | Khushbakht | gold | 09_gold_dimensions | | | | | PLANNED | First dimension load |
| R010 | | Khushbakht | gold | 10_gold_facts | | | | | PLANNED | First fact load |
| R011 | | Khushbakht | gold | 10_gold_facts (re-run) | | 0 | 0 | | PLANNED | Idempotency proof |
| R012 | | Khushbakht | gold | 11_gold_optimize | | | | | PLANNED | Before/after evidence |
| R013 | | Waniya | orchestrator | 12: typical incremental run | | | | | PLANNED | FinOps measurement |
| R014 | | Waniya | orchestrator | 12 (re-run) | | 0 | 0 | | PLANNED | Idempotency proof |
| R015 | | Waniya | validation | 13_gold_validation | | | | | PLANNED | FK, duplicates, reconciliation |

## Phase 3 Idempotency Proof
| Test | Run 1 inserted/updated | Run 2 inserted/updated | Duplicate keys? | Result |
|---|---|---|---|---|
| Re-run Gold dimensions | | 0 / 0 | | |
| Re-run Gold facts | | 0 / 0 | | |
| Re-run orchestrator | | 0 / 0 | | |

## Final Gold Counts
| Table | Rows |
|---|---|
| dim_coin | |
| dim_date | |
| dim_hour | 24 |
| dim_scenario | |
| bridge_scenario_coin | |
| fact_market_hourly | |
| fact_coin_daily | |
| fact_portfolio_daily | |

## Phase 3 Screenshots (docs/screenshots/)
| File | Shows |
|---|---|
| gold_tables.png | SHOW TABLES IN crypto.gold |
| optimize_before_after.png | File count and query time before and after OPTIMIZE |
| orchestrator_run.png | 12 output with all layers |
| gold_validation.png | 13 output, all checks PASS |
| spark_dag_fact_coin_daily.png | Query Profile / DAG of the fact_coin_daily aggregation |
| powerbi_model_view.png | One-to-many relationships |
| dashboard_*.png | One screenshot per dashboard page |

## FinOps Measurements (copy from the logs table)
| Run | Duration (s) | Rows read | Rows written |
|---|---|---|---|
| Orchestrator, typical incremental | | | |
| Gold facts only | | | |
