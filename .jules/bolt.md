# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).
## 2026-06-25 - Optimize TinyDB Existence Checks
**Learning:** Using `table.search(query)` forces TinyDB to perform a full table scan and instantiate all matching documents, which is inefficient for simple existence checks.
**Action:** Always use `table.contains(query)` instead of `len(table.search(query)) > 0` or checking the truthiness of the returned list. This short-circuits evaluation, returning True immediately upon finding the first match and significantly improving performance.
## 2026-06-25 - Apply filtering before data transformation
**Learning:** In the `visualizar_cocktails` route, mapping product IDs to names via `listar_cocktails` for all cocktails in the database before applying user-selected filters resulted in significant overhead, as O(N) mapping operations were performed on items that would ultimately be discarded.
**Action:** When filtering data, always apply the filters and limits *before* passing the dataset to transformation functions (like mapping IDs to names). This prevents unnecessary memory allocations and avoids O(N) operations on items that won't be used in the final response.
