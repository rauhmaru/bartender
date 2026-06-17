#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Bebidas e Receitas de Cocktails (versao WEB)
===========================================================

Aplicacao web para cadastro e visualizacao de produtos (bebidas),
com interface no navegador (Flask) e persistencia em SQLite.

Funcionalidades
---------------
- Menu de navegacao com duas opcoes principais:
    * "Cadastrar produto"
    * "Visualizar produto"
- Cadastrar produto:
    * ID automatico, sequencial, formatado com 5 digitos (00001, 00002, ...).
    * Produto (texto, ate 50 caracteres, obrigatorio).
    * Tipo (texto, ate 30 caracteres, obrigatorio).
    * Volume ml (inteiro, 0 a 99999, obrigatorio).
    * Validacao no servidor e insercao no banco.
    * Mensagens de sucesso/erro (flash messages).
- Visualizar produto:
    * Tabela com colunas ID, Produto, Tipo, Volume (ml).
    * ID exibido com 5 digitos.
    * Mensagem adequada quando nao ha produtos.

Requisitos / Dependencias
-------------------------
- Python 3 (testado em 3.10+).
- Flask (instale com: pip install flask).
- sqlite3 faz parte da biblioteca padrao.

Como executar
-------------
    pip install flask
    python3 app.py

Em seguida abra no navegador:  http://127.0.0.1:5000

Na primeira execucao o arquivo de banco "bebidas.db" e criado
automaticamente no mesmo diretorio do script.

Variaveis de ambiente opcionais:
    HOST  (padrao 127.0.0.1)
    PORT  (padrao 5000)
"""

import os
import sqlite3

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

# Caminho do banco de dados: mesmo diretorio do script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bebidas.db")

# Limites de tamanho dos campos (coerentes com o banco).
MAX_PRODUTO = 50
MAX_TIPO = 30
MAX_VOLUME = 99999  # inteiro com ate 5 digitos
MAX_NOME = 60       # nome do cocktail
MAX_TACARIA = 40    # tipo de copo
MAX_QUANTIDADE = 99999.0  # ml por ingrediente

app = Flask(__name__)
# Chave usada apenas para flash messages (sessao). Pode ser sobrescrita por env.
app.secret_key = os.environ.get("SECRET_KEY", "gerenciador-bebidas-dev-key")


# --------------------------------------------------------------------------- #
# Camada de banco de dados
# --------------------------------------------------------------------------- #
def get_db():
    """Retorna a conexao SQLite associada ao contexto da requisicao."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    """Fecha a conexao ao final da requisicao."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas caso ainda nao existam."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS produtos (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto   TEXT    NOT NULL,
                    tipo      TEXT    NOT NULL,
                    volume_ml INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tipos (
                    id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
                """
            )
            # Popula a tabela de tipos com os tipos ja usados nos produtos.
            conn.execute(
                """
                INSERT OR IGNORE INTO tipos (nome)
                SELECT DISTINCT tipo FROM produtos
                WHERE tipo IS NOT NULL AND TRIM(tipo) <> ''
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cocktails (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome    TEXT NOT NULL,
                    tacaria TEXT NOT NULL,
                    receita TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cocktail_ingredientes (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    cocktail_id   INTEGER NOT NULL,
                    produto_id    INTEGER NOT NULL,
                    quantidade_ml REAL    NOT NULL,
                    FOREIGN KEY (cocktail_id) REFERENCES cocktails (id) ON DELETE CASCADE,
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
                """
            )
    except sqlite3.Error as exc:
        raise RuntimeError(f"Falha ao criar/abrir o banco de dados: {exc}") from exc


def proximo_id():
    """Retorna o proximo ID que sera atribuido a um novo registro."""
    cur = get_db().execute("SELECT MAX(id) AS m FROM produtos")
    resultado = cur.fetchone()["m"]
    return (resultado or 0) + 1


def inserir_produto(produto, tipo, volume_ml):
    """Insere um novo produto e retorna o ID gerado."""
    db = get_db()
    cur = db.execute(
        "INSERT INTO produtos (produto, tipo, volume_ml) VALUES (?, ?, ?)",
        (produto, tipo, volume_ml),
    )
    db.commit()
    return cur.lastrowid


def listar_produtos():
    """Retorna a lista de produtos (linhas com id, produto, tipo, volume_ml)."""
    cur = get_db().execute(
        "SELECT id, produto, tipo, volume_ml FROM produtos ORDER BY id"
    )
    return cur.fetchall()


def listar_tipos():
    """Retorna a lista de tipos de produto cadastrados (id, nome)."""
    cur = get_db().execute(
        "SELECT id, nome FROM tipos ORDER BY nome COLLATE NOCASE"
    )
    return cur.fetchall()


def inserir_tipo(nome):
    """Insere um novo tipo de produto e retorna o ID gerado."""
    db = get_db()
    cur = db.execute("INSERT INTO tipos (nome) VALUES (?)", (nome,))
    db.commit()
    return cur.lastrowid


def remover_produto(produto_id):
    """Remove um produto pelo ID."""
    db = get_db()
    db.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    db.commit()


def remover_cocktail(cocktail_id):
    """Remove um cocktail (e seus ingredientes, via cascade) pelo ID."""
    db = get_db()
    db.execute("DELETE FROM cocktails WHERE id = ?", (cocktail_id,))
    db.commit()


def remover_tipo(tipo_id):
    """Remove um tipo de produto pelo ID."""
    db = get_db()
    db.execute("DELETE FROM tipos WHERE id = ?", (tipo_id,))
    db.commit()


def tipo_em_uso(tipo_id):
    """Retorna True se o tipo (pelo ID) estiver em uso por algum produto."""
    db = get_db()
    row = db.execute("SELECT nome FROM tipos WHERE id = ?", (tipo_id,)).fetchone()
    if row is None:
        return False
    usados = db.execute(
        "SELECT 1 FROM produtos WHERE tipo = ? LIMIT 1", (row["nome"],)
    ).fetchone()
    return usados is not None


def inserir_cocktail(nome, tacaria, receita, ingredientes):
    """Insere um cocktail e seus ingredientes numa unica transacao.

    'ingredientes' e uma lista de tuplas (produto_id, quantidade_ml).
    Retorna o ID do cocktail criado.
    """
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO cocktails (nome, tacaria, receita) VALUES (?, ?, ?)",
            (nome, tacaria, receita),
        )
        cocktail_id = cur.lastrowid
        db.executemany(
            "INSERT INTO cocktail_ingredientes (cocktail_id, produto_id, quantidade_ml) "
            "VALUES (?, ?, ?)",
            [(cocktail_id, pid, qtd) for pid, qtd in ingredientes],
        )
        db.commit()
        return cocktail_id
    except sqlite3.Error:
        db.rollback()
        raise


def listar_cocktails():
    """Retorna os cocktails com seus ingredientes agrupados.

    Cada item: dict(id, nome, tacaria, receita, ingredientes=[(produto, qtd)]).
    """
    db = get_db()
    cocktails = db.execute(
        "SELECT id, nome, tacaria, receita FROM cocktails ORDER BY id"
    ).fetchall()

    todos_ingredientes = db.execute(
        """
        SELECT ci.cocktail_id, p.id AS produto_id, p.produto AS produto,
               ci.quantidade_ml AS quantidade_ml
        FROM cocktail_ingredientes ci
        JOIN produtos p ON p.id = ci.produto_id
        ORDER BY ci.id
        """
    ).fetchall()

    ingredientes_por_cocktail = {}
    for ing in todos_ingredientes:
        cid = ing["cocktail_id"]
        if cid not in ingredientes_por_cocktail:
            ingredientes_por_cocktail[cid] = []
        ingredientes_por_cocktail[cid].append(ing)

    resultado = []
    for c in cocktails:
        resultado.append(
            {
                "id": c["id"],
                "nome": c["nome"],
                "tacaria": c["tacaria"],
                "receita": c["receita"],
                "ingredientes": ingredientes_por_cocktail.get(c["id"], []),
            }
        )
    return resultado


# --------------------------------------------------------------------------- #
# Rotas
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    """Pagina inicial: redireciona para o cadastro."""
    return redirect(url_for("cadastrar"))


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    """Tela de cadastro de produto (GET) e processamento do envio (POST)."""
    tipos = listar_tipos()
    if request.method == "POST":
        produto = (request.form.get("produto") or "").strip()
        tipo = (request.form.get("tipo") or "").strip()
        volume_txt = (request.form.get("volume_ml") or "").strip()

        tipos_validos = {t["nome"] for t in tipos}
        erro = _validar(produto, tipo, volume_txt, tipos_validos)
        if erro:
            flash(erro, "erro")
            # Reexibe o formulario preservando o que foi digitado.
            return render_template(
                "cadastrar.html",
                proximo_id=f"{proximo_id():05d}",
                tipos=tipos,
                form={"produto": produto, "tipo": tipo, "volume_ml": volume_txt},
                ativo="cadastrar",
            )

        try:
            novo_id = inserir_produto(produto, tipo, int(volume_txt))
        except (sqlite3.Error, RuntimeError) as exc:
            flash(f"Erro ao salvar no banco: {exc}", "erro")
            return redirect(url_for("cadastrar"))

        flash(f"Produto cadastrado com sucesso! ID: {novo_id:05d}", "sucesso")
        return redirect(url_for("cadastrar"))

    return render_template(
        "cadastrar.html",
        proximo_id=f"{proximo_id():05d}",
        tipos=tipos,
        form={"produto": "", "tipo": "", "volume_ml": ""},
        ativo="cadastrar",
    )


@app.route("/tipos", methods=["GET", "POST"])
def cadastrar_tipo():
    """Tela de cadastro de tipos de produto."""
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        if not nome:
            flash("O campo 'Tipo de produto' e obrigatorio.", "erro")
            return redirect(url_for("cadastrar_tipo"))
        if len(nome) > MAX_TIPO:
            flash(
                f"'Tipo de produto' deve ter no maximo {MAX_TIPO} caracteres.",
                "erro",
            )
            return redirect(url_for("cadastrar_tipo"))
        try:
            inserir_tipo(nome)
        except sqlite3.IntegrityError:
            flash(f"O tipo '{nome}' ja esta cadastrado.", "erro")
            return redirect(url_for("cadastrar_tipo"))
        except (sqlite3.Error, RuntimeError) as exc:
            flash(f"Erro ao salvar no banco: {exc}", "erro")
            return redirect(url_for("cadastrar_tipo"))

        flash(f"Tipo de produto '{nome}' cadastrado com sucesso!", "sucesso")
        return redirect(url_for("cadastrar_tipo"))

    return render_template(
        "cadastrar_tipo.html",
        tipos=listar_tipos(),
        ativo="cadastrar_tipo",
    )


@app.route("/tipos/<int:tipo_id>/remover", methods=["POST"])
def remover_tipo_route(tipo_id):
    """Remove um tipo de produto. Bloqueia se estiver em uso por algum produto."""
    if tipo_em_uso(tipo_id):
        flash(
            "Nao e possivel remover: o tipo esta em uso em um ou mais produtos.",
            "erro",
        )
        return redirect(url_for("cadastrar_tipo"))
    try:
        remover_tipo(tipo_id)
    except (sqlite3.Error, RuntimeError) as exc:
        flash(f"Erro ao remover: {exc}", "erro")
        return redirect(url_for("cadastrar_tipo"))

    flash("Tipo de produto removido com sucesso.", "sucesso")
    return redirect(url_for("cadastrar_tipo"))


@app.route("/visualizar")
def visualizar():
    """Tela de visualizacao dos produtos cadastrados."""
    produtos = listar_produtos()
    return render_template("visualizar.html", produtos=produtos, ativo="visualizar")


@app.route("/visualizar/<int:produto_id>/remover", methods=["POST"])
def remover_produto_route(produto_id):
    """Remove um produto. Bloqueia se ele estiver em uso em alguma receita."""
    try:
        remover_produto(produto_id)
    except sqlite3.IntegrityError:
        flash(
            "Nao e possivel remover: o produto esta em uso em uma ou mais receitas.",
            "erro",
        )
        return redirect(url_for("visualizar"))
    except (sqlite3.Error, RuntimeError) as exc:
        flash(f"Erro ao remover: {exc}", "erro")
        return redirect(url_for("visualizar"))

    flash("Produto removido com sucesso.", "sucesso")
    return redirect(url_for("visualizar"))


@app.route("/receitas/cocktails/adicionar", methods=["GET", "POST"])
def adicionar_cocktail():
    """Adiciona um cocktail: ingredientes (a partir dos produtos), taçaria e receita."""
    produtos = listar_produtos()

    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        tacaria = (request.form.get("tacaria") or "").strip()
        receita = (request.form.get("receita") or "").strip()
        produto_ids = request.form.getlist("produto_id")
        quantidades = request.form.getlist("quantidade")

        erro, ingredientes = _validar_cocktail(
            nome, tacaria, receita, produto_ids, quantidades, produtos
        )
        if erro:
            flash(erro, "erro")
            return render_template(
                "adicionar_cocktail.html",
                produtos=produtos,
                form={"nome": nome, "tacaria": tacaria, "receita": receita},
                ativo="cocktails",
            )

        try:
            novo_id = inserir_cocktail(nome, tacaria, receita, ingredientes)
        except (sqlite3.Error, RuntimeError) as exc:
            flash(f"Erro ao salvar no banco: {exc}", "erro")
            return redirect(url_for("adicionar_cocktail"))

        flash(f"Cocktail '{nome}' adicionado com sucesso! ID: {novo_id:05d}", "sucesso")
        return redirect(url_for("adicionar_cocktail"))

    return render_template(
        "adicionar_cocktail.html",
        produtos=produtos,
        form={"nome": "", "tacaria": "", "receita": ""},
        ativo="cocktails",
    )


@app.route("/receitas/cocktails")
def visualizar_cocktails():
    """Lista os cocktails, com filtro opcional por ingredientes (produtos)."""
    produtos = listar_produtos()

    selecionados = set()
    for valor in request.args.getlist("ingredientes"):
        if valor.isdigit():
            selecionados.add(int(valor))

    cocktails = listar_cocktails()
    if selecionados:
        cocktails = [
            c
            for c in cocktails
            if selecionados <= {ing["produto_id"] for ing in c["ingredientes"]}
        ]

    return render_template(
        "visualizar_cocktails.html",
        cocktails=cocktails,
        produtos=produtos,
        selecionados=selecionados,
        filtro_ativo=bool(selecionados),
        ativo="ver_cocktails",
    )


@app.route("/receitas/cocktails/<int:cocktail_id>/remover", methods=["POST"])
def remover_cocktail_route(cocktail_id):
    """Remove uma receita (cocktail) e seus ingredientes."""
    try:
        remover_cocktail(cocktail_id)
    except (sqlite3.Error, RuntimeError) as exc:
        flash(f"Erro ao remover: {exc}", "erro")
        return redirect(url_for("visualizar_cocktails"))

    flash("Receita removida com sucesso.", "sucesso")
    return redirect(url_for("visualizar_cocktails"))


def _validar(produto, tipo, volume_txt, tipos_validos=None):
    """Valida os campos. Retorna mensagem de erro (str) ou None se tudo ok."""
    if not produto:
        return "O campo 'Produto' e obrigatorio."
    if len(produto) > MAX_PRODUTO:
        return f"'Produto' deve ter no maximo {MAX_PRODUTO} caracteres."
    if not tipo:
        return "O campo 'Tipo' e obrigatorio."
    if len(tipo) > MAX_TIPO:
        return f"'Tipo' deve ter no maximo {MAX_TIPO} caracteres."
    if tipos_validos is not None and tipo not in tipos_validos:
        return "Selecione um tipo de produto valido."
    if not volume_txt:
        return "O campo 'Volume (ml)' e obrigatorio."
    if not volume_txt.isdigit():
        return "'Volume (ml)' deve ser um numero inteiro."
    volume = int(volume_txt)
    if volume < 0 or volume > MAX_VOLUME:
        return f"'Volume (ml)' deve estar entre 0 e {MAX_VOLUME}."
    return None


def _validar_cocktail(nome, tacaria, receita, produto_ids, quantidades, produtos):
    """Valida os dados do cocktail.

    Retorna (mensagem_erro, ingredientes). Em caso de sucesso a mensagem e None
    e 'ingredientes' e uma lista de tuplas (produto_id, quantidade_ml).
    """
    if not nome:
        return "O campo 'Nome do cocktail' e obrigatorio.", []
    if len(nome) > MAX_NOME:
        return f"'Nome do cocktail' deve ter no maximo {MAX_NOME} caracteres.", []
    if not tacaria:
        return "O campo 'Taçaria' e obrigatorio.", []
    if len(tacaria) > MAX_TACARIA:
        return f"'Taçaria' deve ter no maximo {MAX_TACARIA} caracteres.", []
    if not receita:
        return "O campo 'Receita' e obrigatorio.", []

    ids_validos = {p["id"] for p in produtos}
    ingredientes = []
    for pid_txt, qtd_txt in zip(produto_ids, quantidades):
        pid_txt = (pid_txt or "").strip()
        qtd_txt = (qtd_txt or "").strip().replace(",", ".")
        # Ignora linhas totalmente vazias.
        if not pid_txt and not qtd_txt:
            continue
        if not pid_txt:
            return "Selecione o produto de todos os ingredientes.", []
        try:
            pid = int(pid_txt)
        except ValueError:
            return "Ingrediente invalido.", []
        if pid not in ids_validos:
            return "Ingrediente invalido: produto nao cadastrado.", []
        if not qtd_txt:
            return "Informe a quantidade (ml) de cada ingrediente.", []
        try:
            qtd = float(qtd_txt)
        except ValueError:
            return "'Quantidade' deve ser um numero (ml).", []
        if qtd <= 0 or qtd > MAX_QUANTIDADE:
            return f"'Quantidade' deve ser maior que 0 e ate {int(MAX_QUANTIDADE)}.", []
        ingredientes.append((pid, qtd))

    if not ingredientes:
        return "Adicione pelo menos um ingrediente.", []
    return None, ingredientes


# Disponibiliza os limites para os templates (atributos maxlength etc.).
@app.context_processor
def inject_limits():
    return {
        "MAX_PRODUTO": MAX_PRODUTO,
        "MAX_TIPO": MAX_TIPO,
        "MAX_VOLUME": MAX_VOLUME,
        "MAX_NOME": MAX_NOME,
        "MAX_TACARIA": MAX_TACARIA,
        "MAX_QUANTIDADE": MAX_QUANTIDADE,
    }


def main():
    """Ponto de entrada: inicializa o banco e sobe o servidor."""
    init_db()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
