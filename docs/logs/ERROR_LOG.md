# Error Log

Append new rows at the bottom. Do not rewrite old rows.

| ID | Date | Reported By | File/Cell | Error Message | Cause | Fix | Fixed By | Status |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-10-10 | Khushbakht | 01_logging_utils | NameError: name 'T_BRONZE' is not defined | "# MAGIC %run" pasted as a comment, so 00 never loaded | Put "%run ./00_config_schemas" alone in its own first cell | Khushbakht | Closed |
| E002 | 2026-10-10 | Khushbakht | 00_config_schemas | Paths pointed to missing folders | FULL_DIR/INC_DIR assumed subfolders, files sit directly in raw_files | Set FULL_FILE and INC_FILE to /Volumes/crypto/bronze/raw_files/<filename> | Khushbakht | Closed |
| E003 | | | | | | | | Open |
