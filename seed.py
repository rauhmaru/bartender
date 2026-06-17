#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed de dados — 30 receitas de coqueteis refrescantes (NoSQL / TinyDB).

Cadastra primeiro os produtos (ingredientes) e depois as 30 receitas,
relacionando cada ingrediente a um produto cadastrado.

Drinks com base em gin, rum, vodka, whisky e cachaca (6 de cada).

Uso:
    python3 seed.py

O script e seguro para rodar mais de uma vez:
- Produtos ja existentes (mesmo nome) nao sao duplicados.
- Cocktails ja existentes (mesmo nome) sao ignorados.
"""

from app import (
    app,
    inserir_cocktail,
    inserir_produto,
    inserir_tipo,
    listar_cocktails,
    listar_produtos,
    listar_tipos,
)

# --------------------------------------------------------------------------- #
# Produtos (ingredientes): (nome, tipo, volume_ml de referencia)
# --------------------------------------------------------------------------- #
PRODUTOS = [
    # Destilados
    ("Gin", "Destilado", 750),
    ("Rum Branco", "Destilado", 750),
    ("Rum Escuro", "Destilado", 750),
    ("Vodka", "Destilado", 750),
    ("Whisky Bourbon", "Destilado", 750),
    ("Cachaca", "Destilado", 700),
    # Refrigerantes / agua
    ("Agua Tonica", "Refrigerante", 500),
    ("Agua com Gas", "Refrigerante", 500),
    ("Refrigerante de Cola", "Refrigerante", 350),
    ("Ginger Beer", "Refrigerante", 350),
    ("Ginger Ale", "Refrigerante", 350),
    # Sucos
    ("Suco de Limao", "Suco", 1000),
    ("Suco de Laranja", "Suco", 1000),
    ("Suco de Abacaxi", "Suco", 1000),
    ("Suco de Cranberry", "Suco", 1000),
    ("Suco de Toranja", "Suco", 1000),
    # Adocantes / xaropes
    ("Xarope de Acucar", "Adocante", 500),
    ("Acucar", "Adocante", 1000),
    ("Granadina", "Xarope", 700),
    # Licores / vinhos / bitters
    ("Licor de Laranja", "Licor", 700),
    ("Licor de Maraschino", "Licor", 700),
    ("Vermute Tinto", "Fortificado", 750),
    ("Vinho Tinto", "Vinho", 750),
    ("Angostura Bitters", "Bitter", 200),
    # Frutas / ervas / vegetais
    ("Hortela", "Erva", 50),
    ("Manjericao", "Erva", 50),
    ("Pepino", "Vegetal", 100),
    ("Morango", "Fruta", 100),
    ("Maracuja", "Fruta", 100),
    ("Limao", "Fruta", 100),
    # Laticinios
    ("Leite de Coco", "Laticinio", 500),
    ("Leite Condensado", "Laticinio", 395),
]

# --------------------------------------------------------------------------- #
# Cocktails: (nome, tacaria, receita, [(produto, quantidade_ml), ...])
# --------------------------------------------------------------------------- #
COCKTAILS = [
    # ----------------------------- GIN -----------------------------------
    (
        "Gin Tonica",
        "Taca de gin",
        "Encha a taca com gelo, adicione o gin e complete com a agua tonica. "
        "Finalize espremendo o limao e decore com rodelas.",
        [("Gin", 50), ("Agua Tonica", 150), ("Limao", 10)],
    ),
    (
        "Tom Collins",
        "Copo Collins",
        "Misture gin, suco de limao e xarope com gelo, coe no copo com gelo "
        "e complete com agua com gas. Decore com limao.",
        [("Gin", 50), ("Suco de Limao", 25), ("Xarope de Acucar", 15), ("Agua com Gas", 60)],
    ),
    (
        "Gin Basil Smash",
        "Copo baixo",
        "Macere o manjericao com o xarope, adicione gin e suco de limao, "
        "bata com gelo e coe sobre gelo fresco.",
        [("Gin", 50), ("Suco de Limao", 25), ("Xarope de Acucar", 20), ("Manjericao", 8)],
    ),
    (
        "Cucumber Gin Cooler",
        "Copo highball",
        "Macere o pepino, adicione gin, suco de limao e xarope, bata com gelo, "
        "coe no copo com gelo e complete com agua com gas.",
        [
            ("Gin", 50),
            ("Pepino", 30),
            ("Suco de Limao", 20),
            ("Xarope de Acucar", 15),
            ("Agua com Gas", 60),
        ],
    ),
    (
        "Gin Fizz",
        "Copo highball",
        "Bata gin, suco de limao e xarope com gelo, coe no copo e complete "
        "com agua com gas bem gelada.",
        [("Gin", 50), ("Suco de Limao", 25), ("Xarope de Acucar", 15), ("Agua com Gas", 80)],
    ),
    (
        "Southside",
        "Taca coupe",
        "Bata gin, suco de limao, xarope e hortela com gelo e coe na taca. "
        "Decore com folhas de hortela.",
        [("Gin", 50), ("Suco de Limao", 25), ("Xarope de Acucar", 20), ("Hortela", 6)],
    ),
    # ----------------------------- RUM -----------------------------------
    (
        "Mojito",
        "Copo highball",
        "Macere a hortela com o xarope e o suco de limao, adicione o rum e gelo, "
        "complete com agua com gas e mexa.",
        [
            ("Rum Branco", 50),
            ("Suco de Limao", 25),
            ("Xarope de Acucar", 20),
            ("Hortela", 8),
            ("Agua com Gas", 60),
        ],
    ),
    (
        "Daiquiri",
        "Taca coupe",
        "Bata rum, suco de limao e xarope com bastante gelo e coe na taca gelada.",
        [("Rum Branco", 60), ("Suco de Limao", 25), ("Xarope de Acucar", 15)],
    ),
    (
        "Cuba Libre",
        "Copo highball",
        "Coloque gelo no copo, adicione o rum e o suco de limao e complete "
        "com refrigerante de cola.",
        [("Rum Branco", 50), ("Refrigerante de Cola", 120), ("Suco de Limao", 10)],
    ),
    (
        "Rum Punch",
        "Copo furacao",
        "Misture os sucos com o rum sobre gelo, adicione a granadina por ultimo "
        "para o efeito degrade.",
        [
            ("Rum Escuro", 50),
            ("Suco de Laranja", 60),
            ("Suco de Abacaxi", 60),
            ("Suco de Limao", 15),
            ("Granadina", 10),
        ],
    ),
    (
        "Hemingway Daiquiri",
        "Taca coupe",
        "Bata todos os ingredientes com gelo e coe na taca. Equilibrio citrico "
        "e levemente amargo da toranja.",
        [
            ("Rum Branco", 50),
            ("Suco de Toranja", 30),
            ("Suco de Limao", 15),
            ("Licor de Maraschino", 10),
            ("Xarope de Acucar", 10),
        ],
    ),
    (
        "Dark 'n' Stormy",
        "Copo highball",
        "Encha o copo com gelo, adicione a ginger beer e o suco de limao e "
        "despeje o rum escuro por cima para formar camadas.",
        [("Rum Escuro", 60), ("Ginger Beer", 120), ("Suco de Limao", 10)],
    ),
    # ---------------------------- VODKA ----------------------------------
    (
        "Moscow Mule",
        "Caneca de cobre",
        "Coloque gelo na caneca, adicione vodka e suco de limao e complete "
        "com ginger beer.",
        [("Vodka", 50), ("Ginger Beer", 120), ("Suco de Limao", 15)],
    ),
    (
        "Cosmopolitan",
        "Taca coupe",
        "Bata todos os ingredientes com gelo e coe na taca gelada. "
        "Decore com raspas de laranja.",
        [
            ("Vodka", 40),
            ("Licor de Laranja", 15),
            ("Suco de Cranberry", 30),
            ("Suco de Limao", 15),
        ],
    ),
    (
        "Sea Breeze",
        "Copo highball",
        "Sobre gelo, adicione a vodka, o suco de cranberry e finalize com "
        "o suco de toranja.",
        [("Vodka", 50), ("Suco de Cranberry", 90), ("Suco de Toranja", 30)],
    ),
    (
        "Screwdriver",
        "Copo highball",
        "Coloque gelo, adicione a vodka e complete com suco de laranja gelado.",
        [("Vodka", 50), ("Suco de Laranja", 120)],
    ),
    (
        "Vodka Tonica",
        "Copo highball",
        "Encha o copo com gelo, adicione a vodka, complete com agua tonica "
        "e espreme o limao.",
        [("Vodka", 50), ("Agua Tonica", 150), ("Limao", 10)],
    ),
    (
        "Caipiroska",
        "Copo baixo",
        "Macere o limao com o acucar, adicione gelo e a vodka e mexa bem.",
        [("Vodka", 50), ("Limao", 30), ("Acucar", 15)],
    ),
    # ---------------------------- WHISKY ---------------------------------
    (
        "Whisky Sour",
        "Copo baixo",
        "Bata whisky, suco de limao e xarope com gelo e coe sobre gelo fresco.",
        [("Whisky Bourbon", 50), ("Suco de Limao", 25), ("Xarope de Acucar", 15)],
    ),
    (
        "Whisky Highball",
        "Copo highball",
        "Encha o copo com gelo, adicione o whisky e complete com agua com gas.",
        [("Whisky Bourbon", 50), ("Agua com Gas", 120)],
    ),
    (
        "Mint Julep",
        "Copo julep",
        "Macere a hortela com o xarope, encha o copo com gelo picado e adicione "
        "o whisky. Mexa ate gelar.",
        [("Whisky Bourbon", 60), ("Xarope de Acucar", 15), ("Hortela", 8)],
    ),
    (
        "John Collins",
        "Copo Collins",
        "Misture whisky, suco de limao e xarope com gelo, coe no copo com gelo "
        "e complete com agua com gas.",
        [
            ("Whisky Bourbon", 50),
            ("Suco de Limao", 25),
            ("Xarope de Acucar", 15),
            ("Agua com Gas", 60),
        ],
    ),
    (
        "Whisky Ginger",
        "Copo highball",
        "Coloque gelo, adicione o whisky e o suco de limao e complete com "
        "ginger ale.",
        [("Whisky Bourbon", 50), ("Ginger Ale", 120), ("Suco de Limao", 10)],
    ),
    (
        "New York Sour",
        "Copo baixo",
        "Bata whisky, suco de limao e xarope com gelo, coe sobre gelo e flutue "
        "o vinho tinto por cima.",
        [
            ("Whisky Bourbon", 50),
            ("Suco de Limao", 25),
            ("Xarope de Acucar", 15),
            ("Vinho Tinto", 15),
        ],
    ),
    # --------------------------- CACHACA ---------------------------------
    (
        "Caipirinha",
        "Copo baixo",
        "Macere o limao com o acucar, encha o copo com gelo e adicione a cachaca. "
        "Mexa bem.",
        [("Cachaca", 60), ("Limao", 30), ("Acucar", 20)],
    ),
    (
        "Caipirinha de Morango",
        "Copo baixo",
        "Macere o morango e o limao com o acucar, adicione gelo e a cachaca e "
        "mexa.",
        [("Cachaca", 50), ("Morango", 40), ("Limao", 15), ("Acucar", 15)],
    ),
    (
        "Caipirinha de Maracuja",
        "Copo baixo",
        "Misture a polpa de maracuja com o acucar, adicione gelo e a cachaca e "
        "mexa bem.",
        [("Cachaca", 50), ("Maracuja", 40), ("Acucar", 15)],
    ),
    (
        "Rabo de Galo",
        "Copo baixo",
        "Misture cachaca, vermute tinto e o bitter com gelo e mexa. Coe ou sirva "
        "com gelo.",
        [("Cachaca", 50), ("Vermute Tinto", 30), ("Angostura Bitters", 2)],
    ),
    (
        "Leblon Smash",
        "Copo baixo",
        "Macere a hortela com o xarope e o suco de limao, adicione a cachaca e "
        "gelo e bata rapidamente.",
        [("Cachaca", 50), ("Suco de Limao", 25), ("Xarope de Acucar", 20), ("Hortela", 6)],
    ),
    (
        "Batida de Coco",
        "Taca",
        "Bata cachaca, leite de coco e leite condensado com gelo ate ficar "
        "cremoso e sirva gelado.",
        [("Cachaca", 50), ("Leite de Coco", 60), ("Leite Condensado", 30)],
    ),
]


def run():
    """Insere produtos e cocktails de forma idempotente."""
    with app.app_context():
        existentes = {p["produto"]: p["id"] for p in listar_produtos()}

        novos_produtos = 0
        for nome, tipo, volume in PRODUTOS:
            if nome not in existentes:
                existentes[nome] = inserir_produto(nome, tipo, volume)
                novos_produtos += 1

        tipos_existentes = {t["nome"] for t in listar_tipos()}
        novos_tipos = 0
        for _, tipo, _ in PRODUTOS:
            if tipo and tipo not in tipos_existentes:
                inserir_tipo(tipo)
                tipos_existentes.add(tipo)
                novos_tipos += 1

        nomes_cocktails = {c["nome"] for c in listar_cocktails()}
        novos_cocktails = 0
        for nome, tacaria, receita, ingredientes in COCKTAILS:
            if nome in nomes_cocktails:
                continue
            ings = [(existentes[prod], qtd) for prod, qtd in ingredientes]
            inserir_cocktail(nome, tacaria, receita, ings)
            novos_cocktails += 1

        print(f"Produtos novos inseridos: {novos_produtos}")
        print(f"Tipos novos inseridos: {novos_tipos}")
        print(f"Cocktails novos inseridos: {novos_cocktails}")
        print(f"Total de produtos: {len(listar_produtos())}")
        print(f"Total de cocktails: {len(listar_cocktails())}")


if __name__ == "__main__":
    run()
