## 2026-06-17 - Adding aria-labels to dynamically generated form elements
**Learning:** Dynamic form elements like "remove ingredient" buttons in lists or tables, where typical labels are insufficient or not directly associated, require proper `aria-label` tags for screen readers to explain what item exactly is being interacted with. Relying only on visual indicators like "x" or generic titles might not convey the specific context to screen reader users without proper labeling.
**Action:** Always ensure that dynamically generated rows with actions (like delete, edit, or remove) contain descriptive text hidden from sight (using classes like `sr-only`) or use `aria-label` describing what is being targeted.

## 2026-06-18 - Making Empty States Actionable
**Learning:** This application previously had simple plain-text empty states (like `<p class="vazio">Nenhum produto cadastrado.</p>`). We discovered that leveraging the existing `.cta-section` component provides a much friendlier and clearer call to action in these scenarios, significantly improving the first-time user experience when their inventory is empty.
**Action:** When creating new views that list items, always use the `.cta-section` component for empty states instead of the generic `.vazio` class. This provides an actionable button to guide the user on their next step.

## 2026-06-18 - Hiding Decorative Emojis and Indicating Current Page
**Learning:** The application makes heavy use of inline emojis for icons. These cause redundant and sometimes confusing announcements for screen reader users (e.g., "Cocktail glass, MEU BAR"). Additionally, navigation links lacked programmatic indication of the active state.
**Action:** Apply `aria-hidden="true"` to any decorative `span` or `div` containing emoji icons. Apply `aria-current="page"` dynamically to active navigation links to properly communicate the active page state to assistive technologies.
