# Performance Learnings

- When listing items from TinyDB that have foreign keys (like cocktails and ingredients), avoid redundant queries.
- Pass already-fetched related tables (e.g. `produtos` list) down to helper functions (like `listar_cocktails`) if the helper function supports it.
- In `app.py`, modifying `cocktails = listar_cocktails()` to `cocktails = listar_cocktails(produtos=produtos)` reduced request time by about ~10-15% (70.8ms to 62.6ms) on a test dataset (1000 produtos, 500 cocktails) by avoiding a duplicate `produtos_table.all()` call.
