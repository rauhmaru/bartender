# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).
## 2026-06-25 - Optimize TinyDB Existence Checks
**Learning:** Using `table.search(query)` forces TinyDB to perform a full table scan and instantiate all matching documents, which is inefficient for simple existence checks.
**Action:** Always use `table.contains(query)` instead of `len(table.search(query)) > 0` or checking the truthiness of the returned list. This short-circuits evaluation, returning True immediately upon finding the first match and significantly improving performance.
## 2026-06-25 - Push down filters and limits before expensive O(N) mapping
**Learning:** In Python, iterating over a large list of dictionaries to perform a mapping operation (like enriching with product names), and then filtering or slicing the result later (`limit` or `subset`) is extremely inefficient because of the allocations and data manipulations for items that will ultimately be discarded. In extreme cases this can be up to 20x slower.
**Action:** Always push down your filters (`selecionados`) and limits/slices (`limit=6`) to occur *before* the expensive dictionary mapping loops. This prevents redundant O(N) operations and unused object allocations.
