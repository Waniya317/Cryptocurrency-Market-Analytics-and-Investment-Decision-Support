# Gold Data Model (Star Schema)

**Owner:** Khushbakht | **Reviewer:** Waniya
**Schema:** crypto.gold

## ER Diagram
````mermaid
erDiagram
    dim_coin ||--o{ fact_market_hourly : coin_key
    dim_date ||--o{ fact_market_hourly : date_key
    dim_hour ||--o{ fact_market_hourly : hour_key
    dim_coin ||--o{ fact_coin_daily : coin_key
    dim_date ||--o{ fact_coin_daily : date_key
    dim_scenario ||--o{ bridge_scenario_coin : scenario_key
    dim_coin ||--o{ bridge_scenario_coin : coin_key
    dim_scenario ||--o{ fact_portfolio_daily : scenario_key
    dim_date ||--o{ fact_portfolio_daily : date_key
````

## dim_coin (grain: one row per coin)
| Column | Type | Key | Description |
|---|---|---|---|
| coin_key | BIGINT | PK | xxhash64(coin_id) |
| coin_id | STRING | Business key | CoinGecko ID |
| coin_name | STRING | | Readable name derived from coin_id |
| is_stablecoin | BOOLEAN | | True for tether, usd-coin, dai, paxos-standard, frax |
| first_seen_ts | TIMESTAMP | | Earliest event_ts in Silver |
| last_seen_ts | TIMESTAMP | | Latest event_ts in Silver |
| load_timestamp | TIMESTAMP | | Gold load time |

## dim_date (grain: one calendar date)
| Column | Type | Key | Description |
|---|---|---|---|
| date_key | INT | PK | yyyymmdd |
| full_date | DATE | | |
| year, quarter, month | INT | | |
| month_name, day_name | STRING | | day_name serves Q4 |
| week_of_year, day_of_month, day_of_week | INT | | |
| is_weekend | BOOLEAN | | |

## dim_hour (grain: 24 rows)
| Column | Type | Key | Description |
|---|---|---|---|
| hour_key | INT | PK | 0-23 (serves Q5) |
| hour_label | STRING | | e.g. "14:00" |
| day_part | STRING | | Night / Morning / Afternoon / Evening |

## dim_scenario (grain: one allocation scenario)
| Column | Type | Key | Description |
|---|---|---|---|
| scenario_key | BIGINT | PK | xxhash64(scenario_name) |
| scenario_name | STRING | | e.g. Equal weight, BTC 60 / ETH 40, Top 5 by market cap, Stablecoin heavy, Altcoin heavy |
| description | STRING | | Plain-language rule |

## bridge_scenario_coin (grain: scenario x coin)
| Column | Type | Key | Description |
|---|---|---|---|
| scenario_key | BIGINT | PK, FK -> dim_scenario | |
| coin_key | BIGINT | PK, FK -> dim_coin | |
| weight | DOUBLE | | Weights sum to 1 per scenario |

## fact_market_hourly (grain: coin x hour)
| Column | Type | Key | Description |
|---|---|---|---|
| coin_key | BIGINT | PK, FK -> dim_coin | |
| event_ts | TIMESTAMP | PK | Hour timestamp |
| date_key | INT | FK -> dim_date | |
| hour_key | INT | FK -> dim_hour | |
| price | DOUBLE | | USD |
| market_cap | DOUBLE | | |
| total_volume | DOUBLE | | |
| prev_price | DOUBLE | | Previous hour's price, same coin |
| hourly_return_pct | DOUBLE | | (price - prev_price) / prev_price * 100 |
| volume_change_pct | DOUBLE | | Change vs previous hour's volume (Q6) |
| is_volume_spike | BOOLEAN | | Volume > coin mean + 2 std (Q6) |
| volume_to_mcap_ratio | DOUBLE | | total_volume / market_cap (Q2) |
| batch_id | STRING | | Source batch |
| load_timestamp | TIMESTAMP | | Gold load time |

## fact_coin_daily (grain: coin x day)
| Column | Type | Key | Description |
|---|---|---|---|
| coin_key | BIGINT | PK, FK -> dim_coin | |
| date_key | INT | PK, FK -> dim_date | |
| open_price, close_price | DOUBLE | | First and last hourly price of the day |
| high_price, low_price, avg_price | DOUBLE | | |
| avg_market_cap | DOUBLE | | Q2 |
| avg_volume | DOUBLE | | Mean hourly volume |
| daily_return_pct | DOUBLE | | (close - open) / open * 100 |
| intraday_range_pct | DOUBLE | | (high - low) / open * 100 |
| volatility_pct | DOUBLE | | Std dev of hourly_return_pct (Q3) |
| hours_count | INT | | Hourly rows in the day |
| load_timestamp | TIMESTAMP | | Gold load time |

## fact_portfolio_daily (grain: scenario x day)
| Column | Type | Key | Description |
|---|---|---|---|
| scenario_key | BIGINT | PK, FK -> dim_scenario | |
| date_key | INT | PK, FK -> dim_date | |
| portfolio_return_pct | DOUBLE | | Sum of weight x daily_return_pct |
| market_condition | STRING | | Bull (market avg > +1%), Bear (< -1%), Sideways. Market avg = equal-weight mean of all coins' daily_return_pct |
| is_high_volatility | BOOLEAN | | Market avg volatility above its median |
| load_timestamp | TIMESTAMP | | Gold load time |

## Optional: fact_prediction (only if the prediction component is built)
| Column | Type | Key | Description |
|---|---|---|---|
| coin_key | BIGINT | PK, FK -> dim_coin | |
| prediction_date_key | INT | PK, FK -> dim_date | |
| predicted_direction | STRING | | UP / DOWN |
| actual_direction | STRING | | Filled when known |
| probability_up | DOUBLE | | Model confidence |
| model_version | STRING | | |

## Refresh strategy
- Dimensions and facts: MERGE INTO on the key, update only when a measure changed.
- Facts are recomputed from Silver (small data), then merged, so re-runs show inserted=0 updated=0.
- fact_coin_daily and fact_portfolio_daily are rebuilt for every date present in Silver, then merged.
- Each run logs layer "gold", rows read/written and execution time to pipeline_execution_logs.

## Optimization
- Liquid clustering: fact_market_hourly CLUSTER BY (coin_key, date_key); fact_coin_daily and fact_portfolio_daily CLUSTER BY (date_key).
- OPTIMIZE after loads. Evidence: docs/screenshots/optimize_before_after.png.
- No partitioning: ~81k rows, far below the size where partitions help.

## Power BI relationships (one-to-many, single direction, dimension -> fact)
dim_coin[coin_key] -> fact_market_hourly, fact_coin_daily, bridge_scenario_coin
dim_date[date_key] -> fact_market_hourly, fact_coin_daily, fact_portfolio_daily
dim_hour[hour_key] -> fact_market_hourly
dim_scenario[scenario_key] -> bridge_scenario_coin, fact_portfolio_daily

## Business questions served
| # | Question | Source | Dashboard page |
|---|---|---|---|
| 1 | Performance over time | fact_coin_daily (close_price, daily_return_pct) | Market Overview |
| 2 | Market cap and trading activity | fact_coin_daily (avg_market_cap, avg_volume), fact_market_hourly (volume_to_mcap_ratio) | Market Overview |
| 3 | Volatility | fact_coin_daily (volatility_pct, intraday_range_pct) | Risk and Performance |
| 4 | Day of week | fact_coin_daily + dim_date (day_name) | Risk and Performance |
| 5 | Hour of day | fact_market_hourly + dim_hour | Intraday Analysis |
| 6 | Volume vs price movement | fact_market_hourly (volume_change_pct, is_volume_spike, hourly_return_pct) | Intraday Analysis |
| 7 | Recent intraday behavior | fact_market_hourly (last 24h) | Intraday Analysis |
| 8 | Recent vs historical | view v_recent_vs_historical (notebook 14) | Intraday Analysis |
| 9 | Predicted direction | fact_prediction (optional) | Decision Support |
| 10 | Model accuracy | fact_prediction (optional) | Decision Support |
| 11 | Allocation under market conditions | fact_portfolio_daily + dim_scenario | Decision Support |
| - | Pipeline health | ops.pipeline_execution_logs, bronze.quarantine (views in 14) | Pipeline Monitoring |

## Limitation
Data covers about 31 days. Day-of-week (Q4) has about 4 samples per weekday and
market conditions (Q11) are short-term, so results are indicative.
