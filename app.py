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
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    """Fecha a conexao ao final da requisicao."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria a tabela 'produtos' caso ainda nao exista."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
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
    if request.method == "POST":
        produto = (request.form.get("produto") or "").strip()
        tipo = (request.form.get("tipo") or "").strip()
        volume_txt = (request.form.get("volume_ml") or "").strip()

        erro = _validar(produto, tipo, volume_txt)
        if erro:
            flash(erro, "erro")
            # Reexibe o formulario preservando o que foi digitado.
            return render_template(
                "cadastrar.html",
                proximo_id=f"{proximo_id():05d}",
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
        form={"produto": "", "tipo": "", "volume_ml": ""},
        ativo="cadastrar",
    )


@app.route("/visualizar")
def visualizar():
    """Tela de visualizacao dos produtos cadastrados."""
    produtos = listar_produtos()
    return render_template("visualizar.html", produtos=produtos, ativo="visualizar")


def _validar(produto, tipo, volume_txt):
    """Valida os campos. Retorna mensagem de erro (str) ou None se tudo ok."""
    if not produto:
        return "O campo 'Produto' e obrigatorio."
    if len(produto) > MAX_PRODUTO:
        return f"'Produto' deve ter no maximo {MAX_PRODUTO} caracteres."
    if not tipo:
        return "O campo 'Tipo' e obrigatorio."
    if len(tipo) > MAX_TIPO:
        return f"'Tipo' deve ter no maximo {MAX_TIPO} caracteres."
    if not volume_txt:
        return "O campo 'Volume (ml)' e obrigatorio."
    if not volume_txt.isdigit():
        return "'Volume (ml)' deve ser um numero inteiro."
    volume = int(volume_txt)
    if volume < 0 or volume > MAX_VOLUME:
        return f"'Volume (ml)' deve estar entre 0 e {MAX_VOLUME}."
    return None


# Disponibiliza os limites para os templates (atributos maxlength etc.).
@app.context_processor
def inject_limits():
    return {"MAX_PRODUTO": MAX_PRODUTO, "MAX_TIPO": MAX_TIPO, "MAX_VOLUME": MAX_VOLUME}


def main():
    """Ponto de entrada: inicializa o banco e sobe o servidor."""
    init_db()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
