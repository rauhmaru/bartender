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

## Missing Global Request Body Size Limit
- **Vulnerability**: Missing `MAX_CONTENT_LENGTH` configuration in Flask apps.
- **Risk**: Without a limit on the request body size, the server is vulnerable to Denial of Service (DoS) attacks. Attackers can upload large files or send huge payloads, exhausting server memory and causing crashes.
- **Fix**: Set `app.config['MAX_CONTENT_LENGTH'] = <size>` immediately after app initialization. Example for 16MB: `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024`.
- **Validation**: Write tests using `pytest` to send a payload slightly larger than the limit and ensure a `413 Request Entity Too Large` error is returned.
## 2024-06-18 - [Race Condition in ID Generation (TOCTOU)]
**Vulnerability:**
Fetching the next sequential ID by querying all items and finding the maximum, then immediately inserting using that ID.

**Learning:**
In a multi-threaded web application context (like Flask), concurrent requests might read the exact same maximum ID at the same time, leading to duplicate sequential IDs or write collisions in the underlying database (TinyDB).

**Prevention:**
Introduce an explicit `threading.Lock` within the application logic. The operations of computing the next ID and the subsequent document insertion *must* be atomically wrapped within a `with lock:` context to ensure data consistency across multiple worker threads. This also applies to checks for record existence before an insertion.
## 2026-06-18 - [Security Headers Enhancement]
**Vulnerability:** Missing security headers on HTTP responses, potentially allowing for XSS, clickjacking, or MIME-sniffing attacks.
**Learning:** Adding security headers in Flask can be easily done globally using an `@app.after_request` hook, which provides defense-in-depth across the entire application without needing to modify individual routes.
**Prevention:** Implement the `@app.after_request` pattern to inject headers like `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, and `Content-Security-Policy` into all responses by default.
