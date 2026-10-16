# Work Log

Append new rows at the bottom. Do not rewrite old rows.

| Date | Person | Task | Time Spent | Outcome | Next Step |
|---|---|---|---|---|---|
| 2026-10-10 | Khushbakht | Project planning, roadmap, task split | | Plan + docs drafted | Databricks setup |
| 2026-10-10 | Khushbakht | Databricks setup: catalog crypto, schemas, Volume, JSON upload, Git folder | | Done | Write 00/01 |
| 2026-10-10 | Khushbakht | Inspected JSON structure (inspect_json) | | Found data[] with 5 fields | Write schemas |
| 2026-10-10 | Khushbakht | Wrote + fixed notebooks 00, 01 (%run + paths) | | Tables created | Bronze loads |
| 2026-10-10 | Khushbakht | Ran 02 full load, 03 incremental, re-run test | | All working, see PIPELINE_RUN_LOG | Screenshots, push |
| 2026-10-10 | Khushbakht | Took screenshots, pushed notebooks 00-03 to GitHub | | Done | Upload MD docs + screenshots |
| 2026-10-10 | Khushbakht | Uploaded all MD docs + screenshots to GitHub, added Git rules 10-14 | | Done | Waniya clones + starts Silver |
| 2026-10-10 | Khushbakht | Uploaded run screenshots, filled PIPELINE_RUN_LOG with real counts | | Bronze proof complete | Waniya starts Silver |
| 2026-10-10 | Waniya | Implemented and ran Silver transformation notebook (04_silver_transform) | | 66401 records inserted successfully; Silver table populated | Run Silver re-run test |
| 2026-10-10 | Waniya | Re-ran Silver transformation to verify idempotency | | 0 rows inserted and 0 updated; re-run successful | Document results |
| 2026-10-10 | Waniya | Ran backfill runner for 2026-09-04 to 2026-10-04 | | Backfill completed successfully | Verify execution logs |
| 2026-10-10 | Waniya | Ran schema-drift check on full-load JSON | | Check completed successfully; 0 rows inserted or updated | Verify quarantine and results |
| 2026-10-11 | Waniya | Ran pipeline validation checks | | Validation passed; Bronze 66401 records, Silver 66401 records, quarantine 0 | Record validation results |
| 2026-10-11 | Waniya | Captured and uploaded four pipeline screenshots | | silver_transform, backfill_runner, schema_drift, validation_checks screenshots uploaded | Verify screenshot paths in repository |
| 2026-10-11 | Waniya | Updated DATA_MODEL.md, ERROR_LOG.md, PIPELINE_RUN_LOG.md, and VISUALIZATION_LOG.md | | Documentation updated with pipeline results and validation evidence | Review remaining documentation and commit changes to GitHub 
| 2026-10-16 | Khushbakht | Rebalanced Phase 3 split, kept Phase 2 content in plan docs, mapped 11 business questions to Gold | | Docs ready | Build 08-11 |
| 2026-10-16 | Waniya | | | | |
