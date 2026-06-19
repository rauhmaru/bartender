## Performance Optimizations
- Replaced `table.search()` with `table.get()` in TinyDB table lookups across `app.py`.
- `table.search()` is meant for finding multiple records and always performs a full table scan.
- `table.get()` is specifically designed for single record lookups and features an early exit, halting iteration over documents the moment a match is found.
