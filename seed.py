#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed de dados — 30 receitas de coquetéis refrescantes.

Cadastra primeiro os produtos (ingredientes) e depois as 30 receitas,
relacionando cada ingrediente a um produto cadastrado.

Drinks com base em gin, rum, vodka, whisky e cachaça (6 de cada).

Uso:
    python3 seed.py

O script é seguro para rodar mais de uma vez:
- Produtos já existentes (mesmo nome) não são duplicados.
- Cocktails já existentes (mesmo nome) são ignorados.
"""

from app import (
    app,
    init_db,
    inserir_cocktail,
    inserir_produto,
    inserir_tipo,
    listar_cocktails,
    listar_produtos,
    listar_tipos,
)

# --------------------------------------------------------------------------- #
# Produtos (ingredientes): (nome, tipo, volume_ml de referência)
# --------------------------------------------------------------------------- #
PRODUTOS = [
    # Destilados
    ("Gin", "Destilado", 750),
    ("Rum Branco", "Destilado", 750),
    ("Rum Escuro", "Destilado", 750),
    ("Vodka", "Destilado", 750),
    ("Whisky Bourbon", "Destilado", 750),
    ("Cachaça", "Destilado", 700),
    # Refrigerantes / água
    ("Água Tônica", "Refrigerante", 500),
    ("Água com Gás", "Refrigerante", 500),
    ("Refrigerante de Cola", "Refrigerante", 350),
    ("Ginger Beer", "Refrigerante", 350),
    ("Ginger Ale", "Refrigerante", 350),
    # Sucos
    ("Suco de Limão", "Suco", 1000),
    ("Suco de Laranja", "Suco", 1000),
    ("Suco de Abacaxi", "Suco", 1000),
    ("Suco de Cranberry", "Suco", 1000),
    ("Suco de Toranja", "Suco", 1000),
    # Adoçantes / xaropes
    ("Xarope de Açúcar", "Adoçante", 500),
    ("Açúcar", "Adoçante", 1000),
    ("Granadina", "Xarope", 700),
    # Licores / vinhos / bitters
    ("Licor de Laranja", "Licor", 700),
    ("Licor de Maraschino", "Licor", 700),
    ("Vermute Tinto", "Fortificado", 750),
    ("Vinho Tinto", "Vinho", 750),
    ("Angostura Bitters", "Bitter", 200),
    # Frutas / ervas / vegetais
    ("Hortelã", "Erva", 50),
    ("Manjericão", "Erva", 50),
    ("Pepino", "Vegetal", 100),
    ("Morango", "Fruta", 100),
    ("Maracujá", "Fruta", 100),
    ("Limão", "Fruta", 100),
    # Laticínios
    ("Leite de Coco", "Laticínio", 500),
    ("Leite Condensado", "Laticínio", 395),
]

# --------------------------------------------------------------------------- #
# Cocktails: (nome, taçaria, receita, [(produto, quantidade_ml), ...])
# --------------------------------------------------------------------------- #
COCKTAILS = [
    # ----------------------------- GIN -----------------------------------
    (
        "Gin Tônica",
        "Taça de gin",
        "Encha a taça com gelo, adicione o gin e complete com a água tônica. "
        "Finalize espremendo o limão e decore com rodelas.",
        [("Gin", 50), ("Água Tônica", 150), ("Limão", 10)],
    ),
    (
        "Tom Collins",
        "Copo Collins",
        "Misture gin, suco de limão e xarope com gelo, coe no copo com gelo "
        "e complete com água com gás. Decore com limão.",
        [("Gin", 50), ("Suco de Limão", 25), ("Xarope de Açúcar", 15), ("Água com Gás", 60)],
    ),
    (
        "Gin Basil Smash",
        "Copo baixo",
        "Macere o manjericão com o xarope, adicione gin e suco de limão, "
        "bata com gelo e coe sobre gelo fresco.",
        [("Gin", 50), ("Suco de Limão", 25), ("Xarope de Açúcar", 20), ("Manjericão", 8)],
    ),
    (
        "Cucumber Gin Cooler",
        "Copo highball",
        "Macere o pepino, adicione gin, suco de limão e xarope, bata com gelo, "
        "coe no copo com gelo e complete com água com gás.",
        [
            ("Gin", 50),
            ("Pepino", 30),
            ("Suco de Limão", 20),
            ("Xarope de Açúcar", 15),
            ("Água com Gás", 60),
        ],
    ),
    (
        "Gin Fizz",
        "Copo highball",
        "Bata gin, suco de limão e xarope com gelo, coe no copo e complete "
        "com água com gás bem gelada.",
        [("Gin", 50), ("Suco de Limão", 25), ("Xarope de Açúcar", 15), ("Água com Gás", 80)],
    ),
    (
        "Southside",
        "Taça coupe",
        "Bata gin, suco de limão, xarope e hortelã com gelo e coe na taça. "
        "Decore com folhas de hortelã.",
        [("Gin", 50), ("Suco de Limão", 25), ("Xarope de Açúcar", 20), ("Hortelã", 6)],
    ),
    # ----------------------------- RUM -----------------------------------
    (
        "Mojito",
        "Copo highball",
        "Macere a hortelã com o xarope e o suco de limão, adicione o rum e gelo, "
        "complete com água com gás e mexa.",
        [
            ("Rum Branco", 50),
            ("Suco de Limão", 25),
            ("Xarope de Açúcar", 20),
            ("Hortelã", 8),
            ("Água com Gás", 60),
        ],
    ),
    (
        "Daiquiri",
        "Taça coupe",
        "Bata rum, suco de limão e xarope com bastante gelo e coe na taça gelada.",
        [("Rum Branco", 60), ("Suco de Limão", 25), ("Xarope de Açúcar", 15)],
    ),
    (
        "Cuba Libre",
        "Copo highball",
        "Coloque gelo no copo, adicione o rum e o suco de limão e complete "
        "com refrigerante de cola.",
        [("Rum Branco", 50), ("Refrigerante de Cola", 120), ("Suco de Limão", 10)],
    ),
    (
        "Rum Punch",
        "Copo furacão",
        "Misture os sucos com o rum sobre gelo, adicione a granadina por último "
        "para o efeito degradê.",
        [
            ("Rum Escuro", 50),
            ("Suco de Laranja", 60),
            ("Suco de Abacaxi", 60),
            ("Suco de Limão", 15),
            ("Granadina", 10),
        ],
    ),
    (
        "Hemingway Daiquiri",
        "Taça coupe",
        "Bata todos os ingredientes com gelo e coe na taça. Equilíbrio cítrico "
        "e levemente amargo da toranja.",
        [
            ("Rum Branco", 50),
            ("Suco de Toranja", 30),
            ("Suco de Limão", 15),
            ("Licor de Maraschino", 10),
            ("Xarope de Açúcar", 10),
        ],
    ),
    (
        "Dark 'n' Stormy",
        "Copo highball",
        "Encha o copo com gelo, adicione a ginger beer e o suco de limão e "
        "despeje o rum escuro por cima para formar camadas.",
        [("Rum Escuro", 60), ("Ginger Beer", 120), ("Suco de Limão", 10)],
    ),
    # ---------------------------- VODKA ----------------------------------
    (
        "Moscow Mule",
        "Caneca de cobre",
        "Coloque gelo na caneca, adicione vodka e suco de limão e complete "
        "com ginger beer.",
        [("Vodka", 50), ("Ginger Beer", 120), ("Suco de Limão", 15)],
    ),
    (
        "Cosmopolitan",
        "Taça coupe",
        "Bata todos os ingredientes com gelo e coe na taça gelada. "
        "Decore com raspas de laranja.",
        [
            ("Vodka", 40),
            ("Licor de Laranja", 15),
            ("Suco de Cranberry", 30),
            ("Suco de Limão", 15),
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
        "Vodka Tônica",
        "Copo highball",
        "Encha o copo com gelo, adicione a vodka, complete com água tônica "
        "e espreme o limão.",
        [("Vodka", 50), ("Água Tônica", 150), ("Limão", 10)],
    ),
    (
        "Caipiroska",
        "Copo baixo",
        "Macere o limão com o açúcar, adicione gelo e a vodka e mexa bem.",
        [("Vodka", 50), ("Limão", 30), ("Açúcar", 15)],
    ),
    # ---------------------------- WHISKY ---------------------------------
    (
        "Whisky Sour",
        "Copo baixo",
        "Bata whisky, suco de limão e xarope com gelo e coe sobre gelo fresco.",
        [("Whisky Bourbon", 50), ("Suco de Limão", 25), ("Xarope de Açúcar", 15)],
    ),
    (
        "Whisky Highball",
        "Copo highball",
        "Encha o copo com gelo, adicione o whisky e complete com água com gás.",
        [("Whisky Bourbon", 50), ("Água com Gás", 120)],
    ),
    (
        "Mint Julep",
        "Copo julep",
        "Macere a hortelã com o xarope, encha o copo com gelo picado e adicione "
        "o whisky. Mexa até gelar.",
        [("Whisky Bourbon", 60), ("Xarope de Açúcar", 15), ("Hortelã", 8)],
    ),
    (
        "John Collins",
        "Copo Collins",
        "Misture whisky, suco de limão e xarope com gelo, coe no copo com gelo "
        "e complete com água com gás.",
        [
            ("Whisky Bourbon", 50),
            ("Suco de Limão", 25),
            ("Xarope de Açúcar", 15),
            ("Água com Gás", 60),
        ],
    ),
    (
        "Whisky Ginger",
        "Copo highball",
        "Coloque gelo, adicione o whisky e o suco de limão e complete com "
        "ginger ale.",
        [("Whisky Bourbon", 50), ("Ginger Ale", 120), ("Suco de Limão", 10)],
    ),
    (
        "New York Sour",
        "Copo baixo",
        "Bata whisky, suco de limão e xarope com gelo, coe sobre gelo e flutue "
        "o vinho tinto por cima.",
        [
            ("Whisky Bourbon", 50),
            ("Suco de Limão", 25),
            ("Xarope de Açúcar", 15),
            ("Vinho Tinto", 15),
        ],
    ),
    # --------------------------- CACHAÇA ---------------------------------
    (
        "Caipirinha",
        "Copo baixo",
        "Macere o limão com o açúcar, encha o copo com gelo e adicione a cachaça. "
        "Mexa bem.",
        [("Cachaça", 60), ("Limão", 30), ("Açúcar", 20)],
    ),
    (
        "Caipirinha de Morango",
        "Copo baixo",
        "Macere o morango e o limão com o açúcar, adicione gelo e a cachaça e "
        "mexa.",
        [("Cachaça", 50), ("Morango", 40), ("Limão", 15), ("Açúcar", 15)],
    ),
    (
        "Caipirinha de Maracujá",
        "Copo baixo",
        "Misture a polpa de maracujá com o açúcar, adicione gelo e a cachaça e "
        "mexa bem.",
        [("Cachaça", 50), ("Maracujá", 40), ("Açúcar", 15)],
    ),
    (
        "Rabo de Galo",
        "Copo baixo",
        "Misture cachaça, vermute tinto e o bitter com gelo e mexa. Coe ou sirva "
        "com gelo.",
        [("Cachaça", 50), ("Vermute Tinto", 30), ("Angostura Bitters", 2)],
    ),
    (
        "Leblon Smash",
        "Copo baixo",
        "Macere a hortelã com o xarope e o suco de limão, adicione a cachaça e "
        "gelo e bata rapidamente.",
        [("Cachaça", 50), ("Suco de Limão", 25), ("Xarope de Açúcar", 20), ("Hortelã", 6)],
    ),
    (
        "Batida de Coco",
        "Taça",
        "Bata cachaça, leite de coco e leite condensado com gelo até ficar "
        "cremoso e sirva gelado.",
        [("Cachaça", 50), ("Leite de Coco", 60), ("Leite Condensado", 30)],
    ),
]


def run():
    """Insere produtos e cocktails de forma idempotente."""
    init_db()
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
