# SGDC — Sistema de Gestao de Destilados e Coqueteis

Aplicacao web em Python para cadastro e visualizacao de bebidas/produtos
e receitas de coqueteis, com interface no navegador (Flask) e persistencia
em banco de dados NoSQL (TinyDB).

## Funcionalidades

- **Dashboard "Meu Bar"**
  - Estatisticas: total de itens e coqueteis possiveis.
  - Lista de coqueteis disponiveis ("Pronto para Misturar").
  - Inventario com filtro por tipo e barras de progresso.
- **Cadastrar produto**
  - ID automatico, sequencial, formatado com 5 digitos (00001, 00002, ...).
  - Produto (texto, ate 50 caracteres, obrigatorio).
  - Tipo (selecionavel dos tipos cadastrados, obrigatorio).
  - Volume ml (inteiro, 0 a 99999, obrigatorio).
  - Validacao no servidor e mensagens de sucesso/erro.
- **Listar produtos**
  - Cards com barras de progresso, tipo, volume e botao de remocao.
  - Bloqueio de remocao quando produto esta em uso em receitas.
- **Cadastrar tipo de produto**
  - Lista de tipos com botao de remocao (bloqueia se em uso).
- **Adicionar receitas (coqueteis)**
  - Nome, ingredientes (selecionados a partir dos produtos cadastrados,
    multiplos), quantidade em ml (numerico float por ingrediente),
    tacaria (tipo de copo) e receita (modo de preparo).
- **Visualizar receitas**
  - Cards estilizados com filtro AND de ingredientes.
  - Mensagem dedicada quando nao ha correspondencia.

## Tecnologias

- **Python 3.10+**
- **Flask** (framework web)
- **TinyDB** (banco de dados NoSQL documental, armazenamento em JSON)

## Como executar

```bash
pip install -r requirements.txt
python3 app.py
```

Abra no navegador: <http://127.0.0.1:5000>

O banco `sgdc_db.json` e criado automaticamente na primeira execucao.

### Dados de exemplo (seed)

Para popular o banco com 32 produtos e 30 receitas de coqueteis refrescantes
(gin, rum, vodka, whisky e cachaca):

```bash
python3 seed.py
```

O script e idempotente: produtos e coqueteis ja existentes (mesmo nome) nao
sao duplicados.

### Variaveis de ambiente opcionais

| Variavel     | Padrao      | Descricao                          |
|--------------|-------------|------------------------------------|
| `HOST`       | `127.0.0.1` | Use `0.0.0.0` para acesso na rede. |
| `PORT`       | `5000`      | Porta do servidor.                 |
| `SECRET_KEY` | (dev key)   | Chave para flash messages.         |

## Estrutura

```
app.py                       # servidor Flask (rotas, validacao, TinyDB)
seed.py                      # seed de dados (32 produtos + 30 coqueteis)
requirements.txt             # dependencias
sgdc_db.json                 # banco de dados NoSQL (criado automaticamente)
templates/
  base.html                  # layout base (dark theme + bottom nav)
  dashboard.html             # dashboard "Meu Bar"
  cadastrar.html             # formulario de cadastro de produto
  visualizar.html            # lista de produtos (inventario)
  cadastrar_tipo.html        # cadastro e listagem de tipos
  adicionar_cocktail.html    # formulario de coquetel
  visualizar_cocktails.html  # lista de coqueteis com filtro
```

## Banco de dados (NoSQL — TinyDB)

Os dados sao armazenados em formato JSON no arquivo `sgdc_db.json`.
A estrutura documental e organizada em tres colecoes (tables):

### Colecao `produtos`
```json
{
  "id": 1,
  "produto": "Gin",
  "tipo": "Destilado",
  "volume_ml": 750
}
```

### Colecao `tipos`
```json
{
  "id": 1,
  "nome": "Destilado"
}
```

### Colecao `cocktails`
```json
{
  "id": 1,
  "nome": "Gin Tonica",
  "tacaria": "Taca de gin",
  "receita": "...",
  "ingredientes": [
    {"produto_id": 1, "quantidade_ml": 50},
    {"produto_id": 7, "quantidade_ml": 150}
  ]
}
```

Note que no modelo NoSQL os ingredientes sao embutidos diretamente no
documento do coquetel, eliminando a necessidade de uma tabela de
relacionamento separada (como seria necessario em SQL).
