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
| V006 | 2026-10-17 | Market Overview | Line: close price indexed to 100 by coin | gold.fact_coin_daily, dim_coin, dim_date | close_price, full_date, coin_name | Planned | Q1 |
| V007 | 2026-10-17 | Market Overview | KPI cards: coins tracked, latest total market cap, average daily return | gold.fact_coin_daily | avg_market_cap, daily_return_pct | Planned | Q1, Q2 |
| V008 | 2026-10-17 | Market Overview | Bar: average market cap vs average volume by coin | gold.fact_coin_daily | avg_market_cap, avg_volume | Planned | Q2 |
| V009 | 2026-10-17 | Market Overview | Scatter: volume-to-market-cap ratio vs market cap | gold.fact_market_hourly | volume_to_mcap_ratio, market_cap | Planned | Q2 |
| V010 | 2026-10-17 | Risk and Performance | Bar: volatility by coin (top 15) | gold.fact_coin_daily | volatility_pct, coin_name | Planned | Q3 |
| V011 | 2026-10-17 | Risk and Performance | Column: average daily return by day of week | gold.fact_coin_daily, dim_date | daily_return_pct, day_name | Planned | Q4, about 4 samples per weekday |
| V012 | 2026-10-17 | Risk and Performance | Matrix heatmap: coin x date daily return | gold.fact_coin_daily | daily_return_pct | Planned | Q1, Q3 |
| V013 | 2026-10-17 | Intraday Analysis | Column: average hourly return and volume by hour of day | gold.fact_market_hourly, dim_hour | hourly_return_pct, total_volume, hour_label | Planned | Q5 |
| V014 | 2026-10-17 | Intraday Analysis | Scatter: volume change vs hourly return, spikes highlighted | gold.fact_market_hourly | volume_change_pct, hourly_return_pct, is_volume_spike | Planned | Q6 |
| V015 | 2026-10-17 | Intraday Analysis | Line: last 24 hours price and volume for a selected coin | gold.fact_market_hourly | event_ts, price, total_volume | Planned | Q7 |
| V016 | 2026-10-17 | Intraday Analysis | Clustered column: last 24h vs historical average by hour | v_recent_vs_historical | hour_key, recent_avg, historical_avg | Planned | Q8, view from notebook 14 |
| V017 | 2026-10-17 | Decision Support | Line: cumulative return by allocation scenario | gold.fact_portfolio_daily, dim_scenario | portfolio_return_pct, scenario_name | Planned | Q11 |
| V018 | 2026-10-17 | Decision Support | Matrix: scenario x market condition average return | gold.fact_portfolio_daily | market_condition, portfolio_return_pct | Planned | Q11 |
| V019 | 2026-10-17 | Decision Support | Predicted direction and accuracy | gold.fact_prediction | predicted_direction, actual_direction | Optional | Q9, Q10, only if the prediction component is built |
| V020 | 2026-10-17 | Pipeline Monitoring | Runs by layer and status | crypto.ops.pipeline_execution_logs (view) | layer, status | Planned | Audit visual |
| V021 | 2026-10-17 | Pipeline Monitoring | Rows inserted/updated and duration per run | crypto.ops.pipeline_execution_logs (view) | rows_inserted, rows_updated, start_time, end_time | Planned | Audit visual, FinOps |
| V022 | 2026-10-17 | Pipeline Monitoring | Quarantine reasons | crypto.bronze.quarantine (view) | reason | Planned | Error visual |
| V023 | 2026-10-17 | Pipeline Monitoring | Failed runs table | crypto.ops.pipeline_execution_logs (view) | run_id, error_message | Planned | Error visual |

## Planned Dashboards
1. Market Overview (Q1, Q2)
2. Risk and Performance (Q3, Q4)
3. Intraday Analysis (Q5, Q6, Q7, Q8)
4. Decision Support (Q9, Q10, Q11)
5. Pipeline Monitoring (audit and error logs)
