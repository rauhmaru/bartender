## 2024-06-17 - [Hardcoded Secret Key & Information Leakage]
**Vulnerability:**
1. Hardcoded `SECRET_KEY` fallback in `app.py`.
2. Stack traces / exception details (`{exc}`) were leaked directly into user `flash` messages in `app.py` for multiple endpoints.

**Learning:**
The application was using a hardcoded secret key for development, but leaving it as a fallback in production if the environment variable is not set can lead to session hijacking.
Additionally, leaking raw database exceptions (`Exception as exc`) exposes the internal application logic and database structure to the user.

**Prevention:**
1. Use `os.urandom(24)` or `secrets.token_hex(32)` as a default secure fallback when `SECRET_KEY` is not explicitly set in the environment.
2. Log the actual exception internally using the application logger (`app.logger.error`), and display a generic "Internal server error" or "Database error" message to the end user.
