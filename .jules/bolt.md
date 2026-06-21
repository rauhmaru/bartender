# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).

## 2024-11-20 - TinyDB Existence Checks
**Learning:** Checking for existence in TinyDB using `len(table.search(...)) > 0` or just checking the result of `.search()` evaluates the condition against the entire table, building a list of all matching documents. This can be slow for large tables.
**Action:** Use `table.contains(...)` instead when you only need to know if at least one matching document exists. `contains` will short-circuit and stop iterating as soon as it finds the first match, turning an O(N) full scan into an O(N) scan with early exit.
