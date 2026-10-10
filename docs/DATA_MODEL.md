# Data Model

**Owner:** Waniya
**Reviewer:** Khushbakht
**Last updated:** 2026-10-11

## Source JSON structure
{ source, load_type, frequency, number_of_coins, coins[], start_time, end_time,
  data: [ {coin_id, timestamp, price, market_cap, total_volume}, ... ] }

## Bronze: crypto.bronze.market_data_raw
| Column | Type | Key | Description |
|---|---|---|---|
| coin_id | STRING | Business key | CoinGecko coin ID |
| ts_ms | LONG | Business key | Unix timestamp in ms (JSON field "timestamp") |
| price | DOUBLE | | Price in USD |
| market_cap | DOUBLE | | Market cap |
| total_volume | DOUBLE | | Volume |
| source_file | STRING | | Source file path |
| load_type | STRING | | full / incremental |
| batch_id | STRING | | Run batch ID |
| load_timestamp | TIMESTAMP | | Ingestion time |

Business key: (coin_id, ts_ms)
Load logic: MERGE INTO. Match on the business key. Update only if price, market_cap
or total_volume changed. Otherwise insert. Re-running a file inserts 0 and updates 0.

## Quarantine: crypto.bronze.quarantine
| Column | Type | Description |
|---|---|---|
| raw_record | STRING | Offending record as JSON |
| reason | STRING | "schema drift: extra=[..] missing=[..]" or "null key/price" |
| source_file | STRING | File path |
| batch_id | STRING | Run batch ID |
| load_timestamp | TIMESTAMP | Time quarantined |

## Silver: crypto.silver.market_data_clean
| Column | Type | Key | Description |
|---|---|---|---|
| coin_id | STRING | Primary key (composite) | Coin ID |
| event_ts | TIMESTAMP | Primary key (composite) | Converted from ts_ms |
| price | DOUBLE | | Validated > 0 |
| market_cap | DOUBLE | | Validated >= 0 |
| total_volume | DOUBLE | | Validated >= 0 |
| event_date | DATE | | Derived from event_ts |
| event_hour | INT | | Derived from event_ts |
| batch_id | STRING | | Run batch ID |
| load_timestamp | TIMESTAMP | | Processing time |

Primary key: (coin_id, event_ts)

## Logs: crypto.ops.pipeline_execution_logs
| Column | Type | Description |
|---|---|---|
| run_id | STRING | Unique run ID |
| layer | STRING | bronze / silver / validation |
| file_or_params | STRING | File path, batch ID, bad-row count |
| start_time | TIMESTAMP | Run start |
| end_time | TIMESTAMP | Run end |
| status | STRING | SUCCESS / FAILED |
| rows_inserted | LONG | Rows inserted |
| rows_updated | LONG | Rows updated |
| error_message | STRING | Null on success |


## Cleaning Rules (Silver)

- Filter out records with null `coin_id`, timestamp, or price.
- Keep records where `price >= 0`.
- Keep records where `market_cap` and `total_volume` are either null or non-negative.
- Deduplicate records using `(coin_id, event_ts)`.
- Merge cleaned records into `crypto.silver.market_data_clean`.


## Schema Change History
| Date | Change | Reason | Changed By |
|---|---|---|---|
| 2026-10-10 | Raw JSON field "timestamp" stored as ts_ms | Clear unit (milliseconds) | Khushbakht |


**Data Flow**

1. Full-load and incremental JSON files provide cryptocurrency market data.
2. Bronze ingestion stores raw records in `crypto.bronze.market_data_raw`.
3. Schema-drift and invalid-record checks can send problematic records to `crypto.bronze.quarantine`.
4. Silver transformation validates records, converts timestamps, derives date and hour fields, removes duplicates and merges cleaned records into `crypto.silver.market_data_clean`.
5. Pipeline execution details and errors are recorded in `crypto.ops.pipeline_execution_logs`.
6. Gold-layer details will be added after its implementation is verified.

**Current Validation Status**

**Validation Date:** 2026-10-11  
**Updated By:** Waniya

| Table | Record Count |
|---|---:|
| `crypto.bronze.market_data_raw` | 66,401 |
| `crypto.silver.market_data_clean` | 66,401 |
| `crypto.bronze.quarantine` | 0 |
The pipeline validation checks passed. Bronze and Silver currently contain the same number of records, and the quarantine table contained no records at the time of validation.

## Documentation Update History

| Date | Change | Reason | Changed By |
|---|---|---|---|
| 2026-10-11 | Added data flow and pipeline validation results | Document pipeline implementation and validation performed | Waniya |