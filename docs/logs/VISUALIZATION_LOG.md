# Visualization Log

**Owner:** Waniya
Append new rows at the bottom. Do not rewrite old rows.

| ID | Date | Dashboard | Visual | Source Table | Fields Used | Status | Notes |
|---|---|---|---|---|---|---|---|
| V001 | | Market Overview | Price trend line | gold.* | | Planned | Phase 3 |
| V002 | 2026-10-10 | Pipeline monitoring | Rows inserted per run | crypto.ops.pipeline_execution_logs | start_time, layer, rows_inserted | Optional | Quick Databricks chart |
| V003 | 2026-10-11 | Pipeline monitoring | Bronze and Silver record counts | crypto.bronze.market_data_raw, crypto.silver.market_data_clean | COUNT(*) | Completed query | Both tables contain 66401 records |
| V004 | 2026-10-11 | Pipeline monitoring | Quarantine record count | crypto.bronze.quarantine | COUNT(*) | Completed query | 0 quarantined records at validation time |
| V005 | 2026-10-11 | Pipeline monitoring | Pipeline execution status | crypto.ops.pipeline_execution_logs | run_id, layer, status, rows_inserted, rows_updated | Reviewed | Successful Silver, backfill, and schema-drift runs checked |

## Planned Dashboards
1. Market Overview
2. Risk and Performance
3. Intraday Analysis
4. Decision Support
