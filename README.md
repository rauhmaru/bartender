# Bartender — Gerenciador de Bebidas e Cocktails (Web)

Aplicação web em Python para cadastro e visualização de bebidas/produtos,
com interface no navegador (Flask) e persistência em SQLite.

## Funcionalidades

- **Cadastrar produto**
  - ID automático, sequencial, exibido com 5 dígitos (`00001`, `00002`, ...).
  - Produto (texto, até 50 caracteres, obrigatório).
  - Tipo (texto, até 30 caracteres, obrigatório).
  - Volume ml (inteiro, 0 a 99999, obrigatório).
  - Validação no servidor e mensagens de sucesso/erro.
- **Visualizar produto**
  - Tabela com colunas ID, Produto, Tipo, Volume (ml).
  - Contador de total e mensagem quando não há produtos.
- **Adicionar receitas** (menu suspenso)
  - **Adicionar cocktails**: nome, ingredientes (selecionados a partir dos
    produtos cadastrados, múltiplos), quantidade em ml (numérico float por
    ingrediente), taçaria (tipo de copo) e receita (modo de preparo).
  - **Visualizar cocktails**: lista cada cocktail com ingredientes, quantidades,
    taçaria e receita.

## Requisitos

- Python 3.10+
- Flask (`pip install -r requirements.txt`)
- `sqlite3` faz parte da biblioteca padrão.

## Como executar

```bash
pip install -r requirements.txt
python3 app.py
```

Abra no navegador: <http://127.0.0.1:5000>

O banco `bebidas.db` é criado automaticamente na primeira execução.

### Dados de exemplo (seed)

Para popular o banco com 32 produtos e 30 receitas de coquetéis refrescantes
(gin, rum, vodka, whisky e cachaça):

```bash
python3 seed.py
```

O script é idempotente: produtos e cocktails já existentes (mesmo nome) não são
duplicados.

### Variáveis de ambiente opcionais

| Variável     | Padrão      | Descrição                          |
|--------------|-------------|------------------------------------|
| `HOST`       | `127.0.0.1` | Use `0.0.0.0` para acesso na rede. |
| `PORT`       | `5000`      | Porta do servidor.                 |
| `SECRET_KEY` | (dev key)   | Chave para flash messages.         |

## Estrutura

```
app.py                       # servidor Flask (rotas, validação, SQLite)
requirements.txt             # dependências
templates/
  base.html                  # layout + navegação + estilos
  cadastrar.html             # formulário de cadastro de produto
  visualizar.html            # tabela de produtos
  adicionar_cocktail.html    # formulário de cocktail (ingredientes dinâmicos)
  visualizar_cocktails.html  # lista de cocktails
```

## Banco de dados

Tabela `produtos`:

| Campo       | Tipo                              |
|-------------|-----------------------------------|
| `id`        | INTEGER PRIMARY KEY AUTOINCREMENT |
| `produto`   | TEXT (até 50)                     |
| `tipo`      | TEXT (até 30)                     |
| `volume_ml` | INTEGER (0–99999)                 |

Tabela `cocktails`:

| Campo     | Tipo                              |
|-----------|-----------------------------------|
| `id`      | INTEGER PRIMARY KEY AUTOINCREMENT |
| `nome`    | TEXT                              |
| `tacaria` | TEXT                              |
| `receita` | TEXT                              |

Tabela `cocktail_ingredientes` (relaciona cocktails e produtos):

| Campo           | Tipo                                       |
|-----------------|--------------------------------------------|
| `id`            | INTEGER PRIMARY KEY AUTOINCREMENT          |
| `cocktail_id`   | INTEGER → `cocktails.id` (ON DELETE CASCADE) |
| `produto_id`    | INTEGER → `produtos.id`                     |
| `quantidade_ml` | REAL (float, ml por ingrediente)           |
