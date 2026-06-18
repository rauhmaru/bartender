## Security Journal

### Length Validation
- Always enforce length validation on textual inputs to prevent potential Denial of Service (DoS) or unexpected behavior (e.g., storage issues).
- Apply length limits consistently across both the frontend (`maxlength` attribute) and backend (length checks during form validation).
- When a new limit is introduced (e.g., `MAX_RECEITA`), ensure it is injected into the template context (`inject_limits`) so that it can be applied to the relevant input fields on the frontend.
