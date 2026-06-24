# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).

## 2024-05-14 - TinyDB Table Scans with `.search()`
**Learning:** Checking for existence in TinyDB using `table.search(...)` followed by `if existing:` or `len(usados) > 0` causes a full O(N) table scan, because `.search()` always iterates over every document to return a list of all matches.
**Action:** Always use `table.contains(...)` when checking for existence without needing the actual documents. `.contains()` short-circuits and returns `True` immediately upon finding the first match, resulting in significant performance gains for large tables.
