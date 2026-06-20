## 2026-06-17 - Adding aria-labels to dynamically generated form elements
**Learning:** Dynamic form elements like "remove ingredient" buttons in lists or tables, where typical labels are insufficient or not directly associated, require proper `aria-label` tags for screen readers to explain what item exactly is being interacted with. Relying only on visual indicators like "x" or generic titles might not convey the specific context to screen reader users without proper labeling.
**Action:** Always ensure that dynamically generated rows with actions (like delete, edit, or remove) contain descriptive text hidden from sight (using classes like `sr-only`) or use `aria-label` describing what is being targeted.

## 2026-06-20 - Using CTA for empty states
**Learning:** Using generic plain-text empty states (like "No items found") leaves the user at a dead end without clear next steps. Using actionable empty states (with a `.cta-section` component) provides guidance and clear "call to action" buttons that encourage users to populate the app, improving the flow of the application.
**Action:** When designing or refactoring UI empty states, always prioritize a structured layout with an icon, descriptive text, and a call-to-action button over a simple paragraph text.
