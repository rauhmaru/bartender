---
name: testing-bartender
description: Test the Bartender web app (Flask + SQLite) end-to-end. Use when verifying product/type/recipe management, ingredient filtering, sidebar nav, or removal blocking logic.
---

# Testing the Bartender App

## Prerequisites

- Python 3.10+ with venv
- Flask installed via `requirements.txt`
- Database `bebidas.db` populated (run `python seed.py` if empty)

## Setup

```bash
cd /home/ubuntu/cocktail_manager_web
source .venv/bin/activate
python app.py &   # runs on http://127.0.0.1:5000
```

If the server won't start, check if port 5000 is already in use (`lsof -i :5000`). The app does NOT run in debug mode by default, so template changes require a server restart.

## Devin Secrets Needed

None — the app has no authentication.

## Key Test Scenarios

### 1. Type Management (`/tipos`)
- **Create**: Fill input, click Salvar → green flash `Tipo de produto '<name>' cadastrado com sucesso!`, count increments.
- **Duplicate**: Submit same name → red flash `O tipo '<name>' ja esta cadastrado.`
- **Remove in-use**: Click Remover on a type used by products → red flash `Nao e possivel remover: o tipo esta em uso em um ou mais produtos.` Type stays.
- **Remove unused**: Click Remover on unused type → green flash `Tipo de produto removido com sucesso.` Count decrements.
- **Tip**: All 13 seed types are in-use. To test unused removal, create a test type first, then remove it.

### 2. Product Removal (`/visualizar`)
- Products used in recipes cannot be removed → red flash `Nao e possivel remover: o produto esta em uso em uma ou mais receitas.`
- All 32 seed products are in-use. To test successful removal, you'd need to first remove all recipes using that product.

### 3. Recipe Filter AND Logic (`/receitas/cocktails`)
- Checkboxes select ingredients; filter uses AND (subset check: `selecionados <= ingredient_set`).
- Gin only → 6 recipes (with seed data, minus any removed).
- Gin + Suco de Limão → 5 recipes (Gin Tônica excluded — uses Limão not Suco de Limão).
- Gin + Suco de Limão + Cachaça → 0 recipes → message `Não existem receitas com os ingredientes selecionados.`
- "Limpar filtro" link clears all selections.

### 4. Recipe Removal (`/receitas/cocktails`)
- Each recipe card has a Remover button with JS confirm dialog.
- On removal → green flash `Receita removida com sucesso.`, count decrements, cascade deletes ingredients.

### 5. Sidebar Navigation (all pages)
- Sidebar is sticky (`position: sticky; top: 0; height: 100vh`).
- After scrolling, sidebar stays at top — verify with `getBoundingClientRect().top === 0`.
- 5 links: Cadastrar produtos, Cadastrar tipo de produto, Listar produtos, Cadastrar receitas, Visualizar receitas.
- Active page link has class `ativo`.

## Testing Tips

- **Use Playwright via CDP** (`http://localhost:29229`) for form interactions — the computer tool may have trouble clicking input fields on this app.
- **Confirm dialogs**: Remover buttons use `onsubmit="return confirm(...)"`. In Playwright, handle with `page.on("dialog", lambda d: d.accept())`.
- **Flash messages**: Look for `.flash.sucesso` (green) and `.flash.erro` (red) CSS selectors.
- **Counter text**: Look for `p.vazio` selector — shows count like `13 tipo(s) cadastrado(s).` or `30 cocktail(s) cadastrado(s).`
- **Product IDs**: Gin=1, Rum Branco=2, ..., Cachaça=6, Suco de Limão=12 (used as checkbox values in filter).
- **The app is NOT in debug mode** by default. If you change templates, restart the Flask server to see changes.
- Flash messages in Portuguese — verify exact text (no accents on "Nao", "ja", "e" in flash messages — they use ASCII).
