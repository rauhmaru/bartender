# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).
## 2026-06-25 - Optimize TinyDB Existence Checks
**Learning:** Using `table.search(query)` forces TinyDB to perform a full table scan and instantiate all matching documents, which is inefficient for simple existence checks.
**Action:** Always use `table.contains(query)` instead of `len(table.search(query)) > 0` or checking the truthiness of the returned list. This short-circuits evaluation, returning True immediately upon finding the first match and significantly improving performance.
## 2026-06-25 - Filter Before Formatting
**Learning:** In Python data processing (especially when mapping db structures to view models), performing expensive operations (like dictionary lookups or appending to new lists) on the entire dataset and *then* filtering the result is highly inefficient. It incurs unnecessary overhead for data that will just be discarded.
**Action:** Always apply filters and limits (slicing) *before* performing expensive `O(N)` mappings, formatting, or transformations to minimize CPU usage and memory allocations.
