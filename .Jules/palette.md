## 2026-06-17 - Adding aria-labels to dynamically generated form elements
**Learning:** Dynamic form elements like "remove ingredient" buttons in lists or tables, where typical labels are insufficient or not directly associated, require proper `aria-label` tags for screen readers to explain what item exactly is being interacted with. Relying only on visual indicators like "x" or generic titles might not convey the specific context to screen reader users without proper labeling.
**Action:** Always ensure that dynamically generated rows with actions (like delete, edit, or remove) contain descriptive text hidden from sight (using classes like `sr-only`) or use `aria-label` describing what is being targeted.

## 2026-06-24 - Empty States as Call-to-Actions
**Learning:** Generic text-only empty states like 'Nenhum coquetel cadastrado' miss an opportunity to guide the user. Using a prominent visual component like `.cta-section` to encourage immediate action (e.g., adding a recipe or product) significantly improves usability and onboarding flow.
**Action:** Always replace plain-text empty states with visually engaging `.cta-section` components that include a relevant icon, descriptive title, helpful context, and a clear button to perform the required action.
