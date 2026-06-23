## 2026-06-17 - Adding aria-labels to dynamically generated form elements
**Learning:** Dynamic form elements like "remove ingredient" buttons in lists or tables, where typical labels are insufficient or not directly associated, require proper `aria-label` tags for screen readers to explain what item exactly is being interacted with. Relying only on visual indicators like "x" or generic titles might not convey the specific context to screen reader users without proper labeling.
**Action:** Always ensure that dynamically generated rows with actions (like delete, edit, or remove) contain descriptive text hidden from sight (using classes like `sr-only`) or use `aria-label` describing what is being targeted.

## 2026-06-23 - Empty states should provide actionable next steps
**Learning:** Using simple `.vazio` classes with plain text like "No products found" is unhelpful when a user reaches a list page. Users are more likely to engage with the app and understand its functionality if the empty state provides a clear path forward (e.g., adding an item).
**Action:** Always prefer using the `.cta-section` component over generic plain text for empty states. Ensure the CTA includes a descriptive title, helpful description, and an actionable button (like "Add Item" or "Add Recipe") linking directly to the creation flow.
