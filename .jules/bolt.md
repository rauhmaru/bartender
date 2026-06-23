# Performance Learnings & Patterns

## TinyDB Single Item Lookups
When searching for a single item by a unique ID using `tinydb`, avoid using `table.search(Query.id == id)` as it will perform a full scan of the dataset. Instead, use `table.get(Query.id == id)` which will stop searching and return early upon the first match, resulting in significant speedups (e.g. O(N) scan but halts early, up to ~170x faster if found near the beginning of the list).

## 2024-06-23 - Use contains() instead of search() in TinyDB for existence checks
**Learning:** When checking if a document exists matching a specific condition in TinyDB, using `table.search(Condition)` performs a full table scan and loads all matching documents into memory. Checking if the result has length > 0 is highly inefficient.
**Action:** Use `table.contains(Condition)` instead. This performs a short-circuited evaluation, immediately halting the search upon finding the first match. This saves time and avoids loading unnecessary documents, significantly improving performance for existence checks.
