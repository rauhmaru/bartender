# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).
## 2026-06-25 - Optimize TinyDB Existence Checks
**Learning:** Using `table.search(query)` forces TinyDB to perform a full table scan and instantiate all matching documents, which is inefficient for simple existence checks.
**Action:** Always use `table.contains(query)` instead of `len(table.search(query)) > 0` or checking the truthiness of the returned list. This short-circuits evaluation, returning True immediately upon finding the first match and significantly improving performance.

## 2023-10-25 - Filter Before Expensive O(N) Mapping
**Learning:** In `visualizar_cocktails`, filtering after calling `listar_cocktails` meant that expensive dictionary lookups and dictionary building were performed for all cocktails, even those that would be discarded by the filter.
**Action:** Apply filters to raw database rows (`cocktails_table.all()`) *before* performing expensive mappings (like translating IDs to names), preventing unnecessary object allocation and processing overhead.
