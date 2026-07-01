# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).
## 2026-06-25 - Optimize TinyDB Existence Checks
**Learning:** Using `table.search(query)` forces TinyDB to perform a full table scan and instantiate all matching documents, which is inefficient for simple existence checks.
**Action:** Always use `table.contains(query)` instead of `len(table.search(query)) > 0` or checking the truthiness of the returned list. This short-circuits evaluation, returning True immediately upon finding the first match and significantly improving performance.
## 2026-06-25 - Filter Before Mapping for Data Transformations
**Learning:** In `visualizar_cocktails`, filtering after mapping product IDs to names incurred significant overhead because the expensive O(N) mapping process was executed for all records, even those eventually discarded by the filter.
**Action:** When filtering and transforming data sets, always apply the filter to the raw data *before* performing expensive transformations (like dictionary lookups or ID mapping) to avoid unnecessary processing on discarded items.
