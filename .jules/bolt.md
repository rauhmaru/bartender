## 2024-05-14 - TinyDB CachingMiddleware Performance
**Learning:** In a Flask app using TinyDB, reading `.all()` repeatedly on every request leads to a lot of disk I/O because TinyDB reads the JSON file synchronously on every operation. Using `CachingMiddleware` from `tinydb.middlewares` wraps the underlying storage, caches the DB in memory, and only flushes to disk when necessary, which drastically reduces `index()` route load time (e.g. from ~0.33s per 100 requests to ~0.13s per 100 requests).
**Action:** When using TinyDB in an application with high read frequency relative to write frequency, wrap the storage in `CachingMiddleware`.
## TinyDB table existence checking

- **Date:** 2024-05-18
- **Context:** Looking for existence of records using TinyDB
- **Issue:** Using `len(table.search(...)) > 0` performs a full table scan and loads all matching documents into memory before checking the length. This is O(N) where N is the number of documents in the table.
- **Solution:** Use `table.contains(...)` instead. This stops iteration at the first matching document and returns `True`, effectively short-circuiting the scan.
- **Impact:** Can be ~700x faster for matches near the start of the table, and is always as fast or faster than `search()`.
