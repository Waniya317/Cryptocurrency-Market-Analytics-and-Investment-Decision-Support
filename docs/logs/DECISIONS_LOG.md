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
