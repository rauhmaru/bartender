# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).

## 2026-06-22 - Optimizing existence checks in TinyDB
**Learning:** Using `table.search(Query)` to check for existence (e.g. `len(table.search(...)) > 0` or evaluating its truthiness) is inefficient because it performs a full table scan. TinyDB provides `table.contains(Query)` which acts as an early-exit optimization and stops checking as soon as the first matching document is found.
**Action:** Always prefer `table.contains(...)` over `table.search(...)` when you only need to determine if a document matching a query exists, avoiding costly full table scans.
