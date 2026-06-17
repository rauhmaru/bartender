# SGDC — Sistema de Gestão de Destilados e Coquetéis

Aplicação web em Python para cadastro e visualização de bebidas/produtos
e receitas de coquetéis, com interface no navegador (Flask) e persistência
em banco de dados NoSQL (TinyDB).

## Funcionalidades

- **Dashboard "Meu Bar"**
  - Estatísticas: total de itens e coquetéis possíveis.
  - Lista de coquetéis disponíveis ("Pronto para Misturar").
  - Inventário com filtro por tipo.
- **Cadastrar produto**
  - ID automático, sequencial, formatado com 5 dígitos (00001, 00002, ...).
  - Produto (texto, até 50 caracteres, obrigatório).
  - Tipo (selecionável dos tipos cadastrados, obrigatório).
  - Volume ml (inteiro, 0 a 99999, obrigatório).
  - Validação no servidor e mensagens de sucesso/erro.
- **Listar produtos**
  - Cards com tipo, volume e botões de edição/remoção.
  - Bloqueio de remoção quando produto está em uso em receitas.
- **Cadastrar tipo de produto**
  - Lista de tipos com botões de edição e remoção (bloqueia se em uso).
  - Edição de tipo com propagação automática para produtos.
- **Adicionar receitas (coquetéis)**
  - Nome, ingredientes (selecionados a partir dos produtos cadastrados,
    múltiplos), quantidade em ml (numérico float por ingrediente),
    taçaria (tipo de copo) e receita (modo de preparo).
- **Visualizar receitas**
  - Cards estilizados com filtro AND de ingredientes.
  - Mensagem dedicada quando não há correspondência.

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

O banco `sgdc_db.json` é criado automaticamente na primeira execução.

### Dados de exemplo (seed)

Para popular o banco com 32 produtos e 30 receitas de coquetéis refrescantes
(gin, rum, vodka, whisky e cachaça):

```bash
python3 seed.py
```

O script é idempotente: produtos e coquetéis já existentes (mesmo nome) não
são duplicados.

### Variáveis de ambiente opcionais

| Variável     | Padrão      | Descrição                          |
|--------------|-------------|------------------------------------|
| `HOST`       | `127.0.0.1` | Use `0.0.0.0` para acesso na rede. |
| `PORT`       | `5000`      | Porta do servidor.                 |
| `SECRET_KEY` | (dev key)   | Chave para flash messages.         |

## Estrutura

```
app.py                       # servidor Flask (rotas, validação, TinyDB)
seed.py                      # seed de dados (32 produtos + 30 coquetéis)
requirements.txt             # dependências
sgdc_db.json                 # banco de dados NoSQL (criado automaticamente)
templates/
  base.html                  # layout base (dark theme + bottom nav)
  dashboard.html             # dashboard "Meu Bar"
  cadastrar.html             # formulário de cadastro de produto
  visualizar.html            # lista de produtos (inventário)
  cadastrar_tipo.html        # cadastro e listagem de tipos
  editar_tipo.html           # edição de tipo de produto
  adicionar_cocktail.html    # formulário de coquetel
  editar_cocktail.html       # edição de coquetel
  editar_produto.html        # edição de produto
  visualizar_cocktails.html  # lista de coquetéis com filtro
```

## Banco de dados (NoSQL — TinyDB)

Os dados são armazenados em formato JSON no arquivo `sgdc_db.json`.
A estrutura documental é organizada em três coleções (tables):

### Coleção `produtos`
```json
{
  "id": 1,
  "produto": "Gin",
  "tipo": "Destilado",
  "volume_ml": 750
}
```

### Coleção `tipos`
```json
{
  "id": 1,
  "nome": "Destilado"
}
```

### Coleção `cocktails`
```json
{
  "id": 1,
  "nome": "Gin Tônica",
  "tacaria": "Taça de gin",
  "receita": "...",
  "ingredientes": [
    {"produto_id": 1, "quantidade_ml": 50},
    {"produto_id": 7, "quantidade_ml": 150}
  ]
}
```

Note que no modelo NoSQL os ingredientes são embutidos diretamente no
documento do coquetel, eliminando a necessidade de uma tabela de
relacionamento separada (como seria necessário em SQL).
