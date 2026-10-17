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
| 2026-10-17 | Gold MERGE compares float measures with a 1e-9 relative tolerance | Recomputed aggregates can differ in the last digits; exact comparison would cause fake updates and break the 0/0 re-run proof | Khushbakht |
| 2026-10-17 | Gold MERGE casts the source to the target table schema | Keeps column types explicit and avoids implicit-cast errors | Khushbakht |
| 2026-10-17 | fact_market_hourly and fact_coin_daily clustered by (coin_key, date_key); fact_portfolio_daily by (date_key) | Dashboards filter by coin and date | Khushbakht |
| 2026-10-17 | dim_scenario and bridge_scenario_coin use NOT MATCHED BY SOURCE DELETE | If scenario membership changes (for example top 5 by market cap), stale rows are removed so weights still sum to 1 | Khushbakht |
| 2026-10-17 | Informational PRIMARY KEY / FOREIGN KEY constraints on Gold tables | Documents the star schema in Unity Catalog and lets Power BI detect relationships; not enforced by Delta | Khushbakht |
