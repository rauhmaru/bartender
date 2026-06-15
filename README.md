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

### Variáveis de ambiente opcionais

| Variável     | Padrão      | Descrição                          |
|--------------|-------------|------------------------------------|
| `HOST`       | `127.0.0.1` | Use `0.0.0.0` para acesso na rede. |
| `PORT`       | `5000`      | Porta do servidor.                 |
| `SECRET_KEY` | (dev key)   | Chave para flash messages.         |

## Estrutura

```
app.py                  # servidor Flask (rotas, validação, SQLite)
requirements.txt        # dependências
templates/
  base.html             # layout + navegação + estilos
  cadastrar.html        # formulário de cadastro
  visualizar.html       # tabela de produtos
```

## Banco de dados

Tabela `produtos`:

| Campo       | Tipo                              |
|-------------|-----------------------------------|
| `id`        | INTEGER PRIMARY KEY AUTOINCREMENT |
| `produto`   | TEXT (até 50)                     |
| `tipo`      | TEXT (até 30)                     |
| `volume_ml` | INTEGER (0–99999)                 |
