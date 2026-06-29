## 2026-06-17 - Adding aria-labels to dynamically generated form elements
**Learning:** Dynamic form elements like "remove ingredient" buttons in lists or tables, where typical labels are insufficient or not directly associated, require proper `aria-label` tags for screen readers to explain what item exactly is being interacted with. Relying only on visual indicators like "x" or generic titles might not convey the specific context to screen reader users without proper labeling.
**Action:** Always ensure that dynamically generated rows with actions (like delete, edit, or remove) contain descriptive text hidden from sight (using classes like `sr-only`) or use `aria-label` describing what is being targeted.

## 2024-06-25 - Using actionable empty states for better UX
**Learning:** Plain-text empty states (like "No products registered") leave users without clear guidance on what to do next. Users find it much easier to interact with the system when empty states include a clear Call-to-Action (CTA) that guides them to populate the empty list or section.
**Action:** Always leverage the existing `.cta-section` component instead of generic plain-text `.vazio` classes for major list views (like inventory or recipes) to provide clear, actionable next steps when the content is empty.

## 2026-06-29 - Semantic HTML for Empty States CTA
**Learning:** Replaced plain-text `.vazio` classes with semantic HTML `.cta-section` components (`<h3>` for titles, `<p>` for descriptions, `aria-hidden` for decorative emojis). Actionable, semantic empty states improve screen reader accessibility and provide much better user guidance.
**Action:** When creating empty states, always use the semantic `.cta-section` pattern to ensure accessibility and provide clear, actionable next steps instead of generic "not found" messages.
