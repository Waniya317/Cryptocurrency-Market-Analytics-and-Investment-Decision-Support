# Error Log

Append new rows at the bottom. Do not rewrite old rows.

| ID | Date | Reported By | File/Cell | Error Message | Cause | Fix | Fixed By | Status |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-10-10 | Khushbakht | 01_logging_utils | NameError: name 'T_BRONZE' is not defined | "# MAGIC %run" pasted as a comment, so 00 never loaded | Put "%run ./00_config_schemas" alone in its own first cell | Khushbakht | Closed |
| E002 | 2026-10-10 | Khushbakht | 00_config_schemas | Paths pointed to missing folders | FULL_DIR/INC_DIR assumed subfolders, files sit directly in raw_files | Set FULL_FILE and INC_FILE to /Volumes/crypto/bronze/raw_files/<filename> | Khushbakht | Closed |
| E003 | 2026-10-10 | Waniya | 02_bronze_full_load | FileNotFoundError: full-load JSON not found | Input JSON file was missing from the configured Databricks volume path | Uploaded/made the file available at the expected path and reran the pipeline successfully | Waniya | Closed |
| E004 | 2026-10-15 | Khushbakht | DATA_MODEL.md vs 04_silver_transform | DATA_MODEL says "remove price <= 0", Silver code keeps price >= 0 | Rule changed in code, doc not updated | Decide one rule, update both | Waniya | Open |
| E005 | 2026-10-15 | Khushbakht | PIPELINE_RUN_LOG R006, R007 | Row counts recorded as unknown | Counts not recorded at run time | Read rows from pipeline_execution_logs and fill the two rows | Waniya | Open |
| E006 | 2026-10-17 | Khushbakht | docs/ | Screenshot names in the run log did not match files in the repo; files sat in docs/, not docs/screenshots/ | Files uploaded via the GitHub web UI with default names | Run log screenshot table corrected; move/rename files into docs/screenshots/ | Khushbakht | Open |
| E007 | 2026-10-17 | Khushbakht | 00_config_schemas (Gold patch cell) | TraitError: The '_control_lock' trait of a DatabricksKernel instance expected a Lock, not NoneType | Databricks serverless notebook session state corrupted (not a code error) | Disconnect and reconnect compute, hard refresh (Ctrl+F5), re-run cells one at a time | Khushbakht | Closed |
| E008 | 2026-10-17 | Khushbakht | GitHub repo | Report.md created in repo root, GOLD_DATA.md and optimize_before_after.png not at the documented paths | Files created via GitHub web UI with different names/locations | Move to docs/REPORT.md, rename to docs/GOLD_DATA_MODEL.md, move image to docs/screenshots/ | Khushbakht | Open |