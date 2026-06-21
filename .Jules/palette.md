## 2026-06-17 - Adding aria-labels to dynamically generated form elements
**Learning:** Dynamic form elements like "remove ingredient" buttons in lists or tables, where typical labels are insufficient or not directly associated, require proper `aria-label` tags for screen readers to explain what item exactly is being interacted with. Relying only on visual indicators like "x" or generic titles might not convey the specific context to screen reader users without proper labeling.
**Action:** Always ensure that dynamically generated rows with actions (like delete, edit, or remove) contain descriptive text hidden from sight (using classes like `sr-only`) or use `aria-label` describing what is being targeted.

## 2026-06-21 - Replacing generic empty states with actionable CTAs
**Learning:** Generic text indicating "no data" (e.g., `<p class="vazio">Nenhum produto cadastrado.</p>`) causes a dead end for users. A cohesive Call to Action (CTA) component providing context, a visually pleasing icon, and an explicit path forward greatly improves onboarding and discovery.
**Action:** When a list or view is empty, replace generic plain text placeholders with an actionable component like `.cta-section`. Ensure decorative elements within the component (like emojis) are hidden from screen readers using `aria-hidden="true"`.
