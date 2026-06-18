#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SGDC - Sistema de Gestão de Destilados e Coquetéis (versão WEB)
================================================================

Aplicação web para cadastro e visualização de produtos (bebidas)
e receitas de coquetéis, com interface no navegador (Flask) e
persistência em banco de dados NoSQL (TinyDB).

Funcionalidades
---------------
- Dashboard com estatísticas (total de itens, coquetéis possíveis)
- Cadastro e listagem de produtos
- Cadastro e listagem de tipos de produto
- Cadastro e visualização de receitas de coquetéis
- Filtro AND de ingredientes nas receitas
- Remoção de produtos, tipos e receitas (com bloqueio de integridade)

Requisitos / Dependências
-------------------------
- Python 3 (testado em 3.10+).
- Flask (pip install flask).
- TinyDB (pip install tinydb).

Como executar
-------------
    pip install -r requirements.txt
    python3 app.py

Em seguida abra no navegador:  http://127.0.0.1:5000

Na primeira execução o arquivo de banco "sgdc_db.json" é criado
automaticamente no mesmo diretório do script.

Variáveis de ambiente opcionais:
    HOST  (padrão 127.0.0.1)
    PORT  (padrão 5000)
"""

import os
import secrets

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from tinydb import TinyDB, Query, where

# Caminho do banco de dados: mesmo diretório do script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sgdc_db.json")

# Limites de tamanho dos campos.
MAX_PRODUTO = 50
MAX_TIPO = 30
MAX_VOLUME = 99999
MAX_NOME = 60
MAX_TACARIA = 40
MAX_QUANTIDADE = 99999.0

app = Flask(__name__)
# SECURITY: Use a secure random token if SECRET_KEY is not provided
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# TinyDB instance
db = TinyDB(DB_PATH, indent=2)
produtos_table = db.table("produtos")
tipos_table = db.table("tipos")
cocktails_table = db.table("cocktails")

Produto = Query()
Tipo = Query()
Cocktail = Query()


# --------------------------------------------------------------------------- #
# Camada de banco de dados (NoSQL / TinyDB)
# --------------------------------------------------------------------------- #
def _next_id(table):
    """Retorna o próximo ID sequencial para a tabela."""
    all_docs = table.all()
    if not all_docs:
        return 1
    return max(doc.get("id", 0) for doc in all_docs) + 1


def proximo_id():
    """Retorna o próximo ID de produtos."""
    return _next_id(produtos_table)


def inserir_produto(produto, tipo, volume_ml):
    """Insere um novo produto e retorna o ID gerado."""
    new_id = _next_id(produtos_table)
    produtos_table.insert({
        "id": new_id,
        "produto": produto,
        "tipo": tipo,
        "volume_ml": volume_ml,
    })
    return new_id


def listar_produtos():
    """Retorna a lista de produtos ordenada por ID."""
    docs = produtos_table.all()
    return sorted(docs, key=lambda d: d.get("id", 0))


def listar_tipos():
    """Retorna a lista de tipos ordenada por nome (case-insensitive)."""
    docs = tipos_table.all()
    return sorted(docs, key=lambda d: d.get("nome", "").lower())


def inserir_tipo(nome):
    """Insere um novo tipo. Levanta ValueError se já existir."""
    existing = tipos_table.search(Tipo.nome == nome)
    if existing:
        raise ValueError(f"O tipo '{nome}' já está cadastrado.")
    new_id = _next_id(tipos_table)
    tipos_table.insert({"id": new_id, "nome": nome})
    return new_id


def obter_produto(produto_id):
    """Retorna um produto pelo ID ou None."""
    results = produtos_table.search(Produto.id == produto_id)
    return results[0] if results else None


def atualizar_produto(produto_id, produto, tipo, volume_ml):
    """Atualiza os campos de um produto existente."""
    produtos_table.update(
        {"produto": produto, "tipo": tipo, "volume_ml": volume_ml},
        Produto.id == produto_id,
    )


def remover_produto(produto_id):
    """Remove um produto pelo ID. Levanta ValueError se em uso."""
    # Check if product is used in any cocktail
    all_cocktails = cocktails_table.all()
    for c in all_cocktails:
        for ing in c.get("ingredientes", []):
            if ing.get("produto_id") == produto_id:
                raise ValueError(
                    "Não é possível remover: o produto está em uso em uma ou mais receitas."
                )
    produtos_table.remove(Produto.id == produto_id)


def obter_cocktail(cocktail_id):
    """Retorna um cocktail pelo ID ou None."""
    results = cocktails_table.search(Cocktail.id == cocktail_id)
    return results[0] if results else None


def atualizar_cocktail(cocktail_id, nome, tacaria, receita, ingredientes):
    """Atualiza um cocktail existente com ingredientes embutidos."""
    cocktails_table.update(
        {
            "nome": nome,
            "tacaria": tacaria,
            "receita": receita,
            "ingredientes": [
                {"produto_id": pid, "quantidade_ml": qtd}
                for pid, qtd in ingredientes
            ],
        },
        Cocktail.id == cocktail_id,
    )


def remover_cocktail(cocktail_id):
    """Remove um cocktail pelo ID."""
    cocktails_table.remove(Cocktail.id == cocktail_id)


def obter_tipo(tipo_id):
    """Retorna um tipo pelo ID ou None."""
    results = tipos_table.search(Tipo.id == tipo_id)
    return results[0] if results else None


def atualizar_tipo(tipo_id, nome):
    """Atualiza o nome de um tipo e propaga para os produtos que o usam."""
    old = obter_tipo(tipo_id)
    if not old:
        raise ValueError("Tipo não encontrado.")
    old_nome = old["nome"]
    existing = tipos_table.search((Tipo.nome == nome) & (Tipo.id != tipo_id))
    if existing:
        raise ValueError(f"O tipo '{nome}' já está cadastrado.")
    tipos_table.update({"nome": nome}, Tipo.id == tipo_id)
    if old_nome != nome:
        produtos_table.update({"tipo": nome}, Produto.tipo == old_nome)


def remover_tipo(tipo_id):
    """Remove um tipo pelo ID."""
    tipos_table.remove(Tipo.id == tipo_id)


def tipo_em_uso(tipo_id):
    """Retorna True se o tipo estiver em uso por algum produto."""
    tipo_doc = tipos_table.search(Tipo.id == tipo_id)
    if not tipo_doc:
        return False
    nome = tipo_doc[0]["nome"]
    return produtos_table.contains(Produto.tipo == nome)


def inserir_cocktail(nome, tacaria, receita, ingredientes):
    """Insere um cocktail com ingredientes embutidos (modelo NoSQL).

    'ingredientes' é uma lista de tuplas (produto_id, quantidade_ml).
    Retorna o ID do cocktail criado.
    """
    new_id = _next_id(cocktails_table)
    cocktails_table.insert({
        "id": new_id,
        "nome": nome,
        "tacaria": tacaria,
        "receita": receita,
        "ingredientes": [
            {"produto_id": pid, "quantidade_ml": qtd}
            for pid, qtd in ingredientes
        ],
    })
    return new_id


def listar_cocktails(produtos=None, cocktails=None):
    """Retorna os cocktails com nomes dos produtos nos ingredientes."""
    if produtos is None:
        produtos = produtos_table.all()
    if cocktails is None:
        cocktails = cocktails_table.all()

    produtos_map = {p["id"]: p["produto"] for p in produtos}
    cocktails = sorted(cocktails, key=lambda d: d.get("id", 0))
    resultado = []
    for c in cocktails:
        ings = []
        for ing in c.get("ingredientes", []):
            ings.append({
                "produto_id": ing["produto_id"],
                "produto": produtos_map.get(ing["produto_id"], "???"),
                "quantidade_ml": ing["quantidade_ml"],
            })
        resultado.append({
            "id": c["id"],
            "nome": c["nome"],
            "tacaria": c["tacaria"],
            "receita": c["receita"],
            "ingredientes": ings,
        })
    return resultado


def contar_coqueteis_possiveis(produtos=None, cocktails=None):
    """Conta quantos coquetéis podem ser preparados (todos ingredientes disponíveis)."""
    if produtos is None:
        produtos = produtos_table.all()
    if cocktails is None:
        cocktails = cocktails_table.all()

    produto_ids = {p["id"] for p in produtos}
    count = 0
    for c in cocktails:
        needed = {ing["produto_id"] for ing in c.get("ingredientes", [])}
        if needed <= produto_ids:
            count += 1
    return count


# --------------------------------------------------------------------------- #
# Rotas
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    """Dashboard principal — Meu Bar."""
    # ⚡ Bolt: Fetch base data once per request to avoid redundant database hits
    produtos = listar_produtos()
    cocktails_db = cocktails_table.all()

    total_itens = len(produtos)
    coqueteis_possiveis = contar_coqueteis_possiveis(produtos, cocktails_db)
    cocktails = listar_cocktails(produtos, cocktails_db)

    # Agrupar produtos por tipo
    tipos_unicos = sorted(set(p["tipo"] for p in produtos))

    return render_template(
        "dashboard.html",
        total_itens=total_itens,
        coqueteis_possiveis=coqueteis_possiveis,
        cocktails=cocktails,
        produtos=produtos,
        tipos_unicos=tipos_unicos,
        ativo="dashboard",
    )


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
            return render_template(
                "cadastrar.html",
                proximo_id=f"{proximo_id():05d}",
                tipos=tipos,
                form={"produto": produto, "tipo": tipo, "volume_ml": volume_txt},
                ativo="produtos",
            )

        try:
            novo_id = inserir_produto(produto, tipo, int(volume_txt))
        except Exception as exc:
            app.logger.error(f"Erro ao salvar produto no banco: {exc}")
            flash("Ocorreu um erro interno ao salvar o produto.", "erro")
            return redirect(url_for("cadastrar"))

        flash(f"Produto cadastrado com sucesso! ID: {novo_id:05d}", "sucesso")
        return redirect(url_for("cadastrar"))

    return render_template(
        "cadastrar.html",
        proximo_id=f"{proximo_id():05d}",
        tipos=tipos,
        form={"produto": "", "tipo": "", "volume_ml": ""},
        ativo="produtos",
    )


@app.route("/tipos", methods=["GET", "POST"])
def cadastrar_tipo():
    """Tela de cadastro de tipos de produto."""
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        if not nome:
            flash("O campo 'Tipo de produto' é obrigatório.", "erro")
            return redirect(url_for("cadastrar_tipo"))
        if len(nome) > MAX_TIPO:
            flash(
                f"'Tipo de produto' deve ter no máximo {MAX_TIPO} caracteres.",
                "erro",
            )
            return redirect(url_for("cadastrar_tipo"))
        try:
            inserir_tipo(nome)
        except ValueError as exc:
            flash(str(exc), "erro")
            return redirect(url_for("cadastrar_tipo"))
        except Exception as exc:
            app.logger.error(f"Erro ao salvar tipo no banco: {exc}")
            flash("Ocorreu um erro interno ao salvar o tipo.", "erro")
            return redirect(url_for("cadastrar_tipo"))

        flash(f"Tipo de produto '{nome}' cadastrado com sucesso!", "sucesso")
        return redirect(url_for("cadastrar_tipo"))

    return render_template(
        "cadastrar_tipo.html",
        tipos=listar_tipos(),
        ativo="tipos",
    )


@app.route("/tipos/<int:tipo_id>/remover", methods=["POST"])
def remover_tipo_route(tipo_id):
    """Remove um tipo de produto. Bloqueia se estiver em uso."""
    if tipo_em_uso(tipo_id):
        flash(
            "Não é possível remover: o tipo está em uso em um ou mais produtos.",
            "erro",
        )
        return redirect(url_for("cadastrar_tipo"))
    try:
        remover_tipo(tipo_id)
    except Exception as exc:
        app.logger.error(f"Erro ao remover tipo: {exc}")
        flash("Ocorreu um erro interno ao remover o tipo.", "erro")
        return redirect(url_for("cadastrar_tipo"))

    flash("Tipo de produto removido com sucesso.", "sucesso")
    return redirect(url_for("cadastrar_tipo"))


@app.route("/tipos/<int:tipo_id>/editar", methods=["GET", "POST"])
def editar_tipo(tipo_id):
    """Tela de edição de tipo de produto."""
    tipo_obj = obter_tipo(tipo_id)
    if not tipo_obj:
        flash("Tipo não encontrado.", "erro")
        return redirect(url_for("cadastrar_tipo"))

    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        if not nome:
            flash("O campo 'Tipo de produto' é obrigatório.", "erro")
            return render_template(
                "editar_tipo.html",
                tipo_obj=tipo_obj,
                form={"nome": nome},
                ativo="tipos",
            )
        if len(nome) > MAX_TIPO:
            flash(
                f"'Tipo de produto' deve ter no máximo {MAX_TIPO} caracteres.",
                "erro",
            )
            return render_template(
                "editar_tipo.html",
                tipo_obj=tipo_obj,
                form={"nome": nome},
                ativo="tipos",
            )
        try:
            atualizar_tipo(tipo_id, nome)
        except ValueError as exc:
            flash(str(exc), "erro")
            return render_template(
                "editar_tipo.html",
                tipo_obj=tipo_obj,
                form={"nome": nome},
                ativo="tipos",
            )
        except Exception as exc:
            app.logger.error(f"Erro ao editar tipo no banco: {exc}")
            flash("Ocorreu um erro interno ao atualizar o tipo.", "erro")
            return redirect(url_for("editar_tipo", tipo_id=tipo_id))

        flash(f"Tipo de produto atualizado com sucesso!", "sucesso")
        return redirect(url_for("cadastrar_tipo"))

    return render_template(
        "editar_tipo.html",
        tipo_obj=tipo_obj,
        form={"nome": tipo_obj["nome"]},
        ativo="tipos",
    )


@app.route("/visualizar")
def visualizar():
    """Tela de visualização dos produtos cadastrados."""
    produtos = listar_produtos()
    return render_template("visualizar.html", produtos=produtos, ativo="produtos")


@app.route("/visualizar/<int:produto_id>/editar", methods=["GET", "POST"])
def editar_produto(produto_id):
    """Tela de edição de produto."""
    prod = obter_produto(produto_id)
    if not prod:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("visualizar"))

    tipos = listar_tipos()

    if request.method == "POST":
        produto = (request.form.get("produto") or "").strip()
        tipo = (request.form.get("tipo") or "").strip()
        volume_txt = (request.form.get("volume_ml") or "").strip()

        tipos_validos = {t["nome"] for t in tipos}
        erro = _validar(produto, tipo, volume_txt, tipos_validos)
        if erro:
            flash(erro, "erro")
            return render_template(
                "editar_produto.html",
                produto_obj=prod,
                tipos=tipos,
                form={"produto": produto, "tipo": tipo, "volume_ml": volume_txt},
                ativo="produtos",
            )

        try:
            atualizar_produto(produto_id, produto, tipo, int(volume_txt))
        except Exception as exc:
            app.logger.error(f"Erro ao atualizar produto no banco: {exc}")
            flash("Ocorreu um erro interno ao atualizar o produto.", "erro")
            return redirect(url_for("editar_produto", produto_id=produto_id))

        flash(f"Produto atualizado com sucesso! ID: {produto_id:05d}", "sucesso")
        return redirect(url_for("visualizar"))

    return render_template(
        "editar_produto.html",
        produto_obj=prod,
        tipos=tipos,
        form={
            "produto": prod["produto"],
            "tipo": prod["tipo"],
            "volume_ml": str(prod["volume_ml"]),
        },
        ativo="produtos",
    )


@app.route("/visualizar/<int:produto_id>/remover", methods=["POST"])
def remover_produto_route(produto_id):
    """Remove um produto. Bloqueia se estiver em uso em alguma receita."""
    try:
        remover_produto(produto_id)
    except ValueError as exc:
        flash(str(exc), "erro")
        return redirect(url_for("visualizar"))
    except Exception as exc:
        app.logger.error(f"Erro ao remover produto: {exc}")
        flash("Ocorreu um erro interno ao remover o produto.", "erro")
        return redirect(url_for("visualizar"))

    flash("Produto removido com sucesso.", "sucesso")
    return redirect(url_for("visualizar"))


@app.route("/receitas/cocktails/adicionar", methods=["GET", "POST"])
def adicionar_cocktail():
    """Adiciona um cocktail."""
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
                ativo="receitas",
            )

        try:
            novo_id = inserir_cocktail(nome, tacaria, receita, ingredientes)
        except Exception as exc:
            app.logger.error(f"Erro ao salvar cocktail no banco: {exc}")
            flash("Ocorreu um erro interno ao salvar o coquetel.", "erro")
            return redirect(url_for("adicionar_cocktail"))

        flash(f"Coquetel '{nome}' adicionado com sucesso!", "sucesso")
        return redirect(url_for("adicionar_cocktail"))

    return render_template(
        "adicionar_cocktail.html",
        produtos=produtos,
        form={"nome": "", "tacaria": "", "receita": ""},
        ativo="receitas",
    )


@app.route("/receitas/cocktails")
def visualizar_cocktails():
    """Lista os cocktails, com filtro opcional por ingredientes."""
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
        ativo="receitas",
    )


@app.route("/receitas/cocktails/<int:cocktail_id>/editar", methods=["GET", "POST"])
def editar_cocktail(cocktail_id):
    """Tela de edição de cocktail."""
    cock = obter_cocktail(cocktail_id)
    if not cock:
        flash("Receita não encontrada.", "erro")
        return redirect(url_for("visualizar_cocktails"))

    produtos = listar_produtos()
    produtos_map = {p["id"]: p["produto"] for p in produtos}

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
            ings_form = []
            for pid_txt, qtd_txt in zip(produto_ids, quantidades):
                pid_txt = (pid_txt or "").strip()
                qtd_txt = (qtd_txt or "").strip()
                if pid_txt or qtd_txt:
                    ings_form.append({"produto_id": int(pid_txt) if pid_txt.isdigit() else 0, "quantidade_ml": qtd_txt})
            return render_template(
                "editar_cocktail.html",
                cocktail=cock,
                produtos=produtos,
                form={"nome": nome, "tacaria": tacaria, "receita": receita},
                ingredientes_form=ings_form if ings_form else cock.get("ingredientes", []),
                ativo="receitas",
            )

        try:
            atualizar_cocktail(cocktail_id, nome, tacaria, receita, ingredientes)
        except Exception as exc:
            app.logger.error(f"Erro ao atualizar cocktail no banco: {exc}")
            flash("Ocorreu um erro interno ao atualizar a receita.", "erro")
            return redirect(url_for("editar_cocktail", cocktail_id=cocktail_id))

        flash(f"Receita '{nome}' atualizada com sucesso!", "sucesso")
        return redirect(url_for("visualizar_cocktails"))

    ings_with_names = []
    for ing in cock.get("ingredientes", []):
        ings_with_names.append({
            "produto_id": ing["produto_id"],
            "quantidade_ml": ing["quantidade_ml"],
        })

    return render_template(
        "editar_cocktail.html",
        cocktail=cock,
        produtos=produtos,
        form={
            "nome": cock["nome"],
            "tacaria": cock["tacaria"],
            "receita": cock["receita"],
        },
        ingredientes_form=ings_with_names,
        ativo="receitas",
    )


@app.route("/receitas/cocktails/<int:cocktail_id>/remover", methods=["POST"])
def remover_cocktail_route(cocktail_id):
    """Remove uma receita (cocktail)."""
    try:
        remover_cocktail(cocktail_id)
    except Exception as exc:
        app.logger.error(f"Erro ao remover cocktail: {exc}")
        flash("Ocorreu um erro interno ao remover a receita.", "erro")
        return redirect(url_for("visualizar_cocktails"))

    flash("Receita removida com sucesso.", "sucesso")
    return redirect(url_for("visualizar_cocktails"))


def _validar(produto, tipo, volume_txt, tipos_validos=None):
    """Valida os campos de produto. Retorna mensagem de erro ou None."""
    if not produto:
        return "O campo 'Produto' é obrigatório."
    if len(produto) > MAX_PRODUTO:
        return f"'Produto' deve ter no máximo {MAX_PRODUTO} caracteres."
    if not tipo:
        return "O campo 'Tipo' é obrigatório."
    if len(tipo) > MAX_TIPO:
        return f"'Tipo' deve ter no máximo {MAX_TIPO} caracteres."
    if tipos_validos is not None and tipo not in tipos_validos:
        return "Selecione um tipo de produto válido."
    if not volume_txt:
        return "O campo 'Volume (ml)' é obrigatório."
    if not volume_txt.isdigit():
        return "'Volume (ml)' deve ser um número inteiro."
    volume = int(volume_txt)
    if volume < 0 or volume > MAX_VOLUME:
        return f"'Volume (ml)' deve estar entre 0 e {MAX_VOLUME}."
    return None


def _validar_cocktail(nome, tacaria, receita, produto_ids, quantidades, produtos):
    """Valida os dados do cocktail."""
    if not nome:
        return "O campo 'Nome do coquetel' é obrigatório.", []
    if len(nome) > MAX_NOME:
        return f"'Nome do coquetel' deve ter no máximo {MAX_NOME} caracteres.", []
    if not tacaria:
        return "O campo 'Taçaria' é obrigatório.", []
    if len(tacaria) > MAX_TACARIA:
        return f"'Taçaria' deve ter no máximo {MAX_TACARIA} caracteres.", []
    if not receita:
        return "O campo 'Receita' é obrigatório.", []

    ids_validos = {p["id"] for p in produtos}
    ingredientes = []
    for pid_txt, qtd_txt in zip(produto_ids, quantidades):
        pid_txt = (pid_txt or "").strip()
        qtd_txt = (qtd_txt or "").strip().replace(",", ".")
        if not pid_txt and not qtd_txt:
            continue
        if not pid_txt:
            return "Selecione o produto de todos os ingredientes.", []
        try:
            pid = int(pid_txt)
        except ValueError:
            return "Ingrediente inválido.", []
        if pid not in ids_validos:
            return "Ingrediente inválido: produto não cadastrado.", []
        if not qtd_txt:
            return "Informe a quantidade (ml) de cada ingrediente.", []
        try:
            qtd = float(qtd_txt)
        except ValueError:
            return "'Quantidade' deve ser um número (ml).", []
        if qtd <= 0 or qtd > MAX_QUANTIDADE:
            return f"'Quantidade' deve ser maior que 0 e ate {int(MAX_QUANTIDADE)}.", []
        ingredientes.append((pid, qtd))

    if not ingredientes:
        return "Adicione pelo menos um ingrediente.", []
    return None, ingredientes


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
    """Ponto de entrada: sobe o servidor."""
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
