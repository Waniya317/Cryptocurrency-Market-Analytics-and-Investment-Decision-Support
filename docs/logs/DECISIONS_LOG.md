# Decisions Log

Append new rows at the bottom. Do not rewrite old rows.

| Date | Decision | Reason | Decided By |
|---|---|---|---|
| 2026-10-10 | Manual JSON ingestion | CoinGecko API blocked on Databricks Free; professor approved | Khushbakht, Waniya |
| 2026-10-10 | Business key = (coin_id, ts_ms) | Unique per coin per hour | Khushbakht, Waniya |
| 2026-10-10 | Explicit schemas, no inference | Phase 2 requirement | Khushbakht, Waniya |
| 2026-10-10 | Khushbakht = Bronze, Waniya = Silver | Even workload | Khushbakht, Waniya |
| 2026-10-10 | Catalog name = crypto; JSON files directly in /Volumes/crypto/bronze/raw_files/ | Matches actual Volume layout | Khushbakht |
| 2026-10-10 | MERGE updates only when values changed | Makes re-runs report 0 inserted, 0 updated (idempotency proof) | Khushbakht |
| 2026-10-10 | Bad records (extra/missing keys, null key/price) go to crypto.bronze.quarantine | Schema drift handling without stopping the load | Khushbakht |
| 2026-10-10 | Shared bronze_load() in 01_logging_utils | 02 and 03 stay short, same logic for both loads | Khushbakht |
| 2026-10-10 | Notebooks start with %run in its own cell | %run only works as a magic cell, not a comment | Khushbakht |
| 2026-10-10 | All MD docs live in GitHub as the single source of truth; log files are append-only | Waniya can clone, update, and push without conflicts or stale copies | Khushbakht, Waniya |
| 2026-10-10 | Silver transformation converts millisecond timestamps into timestamps and derives event_date and event_hour | Supports time-based analysis and consistent Silver data | Waniya |
| 2026-10-10 | Silver records are deduplicated using (coin_id, event_ts) before merging | Prevents duplicate records for the same coin and timestamp | Waniya |
| 2026-10-10 | Backfill runner uses a specified start_date and end_date | Allows historical data to be reprocessed for a selected period | Waniya |
| 2026-10-10 | Schema-drift checks run separately from the standard ingestion process | Helps identify unexpected JSON fields without interrupting normal ingestion | Waniya |
| 2026-10-11 | Pipeline validation includes record counts, duplicate-key checks, null checks, and timestamp checks | Verifies data quality across the Bronze and Silver layers | Waniya |
| 2026-10-16 | Phase 3 split: Khushbakht = notebooks 08-11 + data model/DAG/FinOps; Waniya = 12-14 + Power BI + report export | Notebooks in sequence, equal workload (~15h each) | Khushbakht, Waniya |
| 2026-10-16 | Gold = 4 dims/bridge + 3 facts, incl. fact_portfolio_daily and dim_scenario | Needed for business questions 6 and 11 | Khushbakht |
| 2026-10-16 | Power BI connects directly to Waniya's workspace using a Databricks token | Token option available; one .pbix connects to one workspace | Khushbakht, Waniya |
| 2026-10-17 | Gold data model doc is docs/GOLD_DATA_MODEL.md | One name used by all docs | Khushbakht |
| 2026-10-17 | No partitioning; liquid clustering on key columns + OPTIMIZE | About 81k rows; queries filter by coin and date | Khushbakht |
| 2026-10-17 | coin_key = xxhash64(coin_id) | Deterministic surrogate key keeps MERGE idempotent | Khushbakht |
| 2026-10-17 | Gold facts recomputed from Silver and merged (update only if changed) | Small data, simple and idempotent; watermark/Change Data Feed is the enterprise option | Khushbakht |
| 2026-10-17 | Orchestrator notebook chains 03 -> 04 -> 09 -> 10 and logs layer "orchestrator" | Requirement: Gold refreshes automatically after Silver | Waniya, Khushbakht |
| 2026-10-17 | Dataset has no PII; the Databricks token stays out of GitHub | Public market data; secrets must not be committed | Khushbakht, Waniya |
| 2026-10-17 | Spark analysis uses Query Profile / explain("formatted") if the classic Spark UI is unavailable | Serverless on Free Edition | Khushbakht |
