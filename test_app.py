from app import contar_coqueteis_possiveis

def test_contar_coqueteis_possiveis_empty_lists():
    # Both empty
    assert contar_coqueteis_possiveis(produtos=[], cocktails=[]) == 0

def test_contar_coqueteis_possiveis_cocktail_no_ingredients():
    # If a cocktail has no ingredients, it is possible by default
    cocktails = [{"nome": "Água", "ingredientes": []}]
    assert contar_coqueteis_possiveis(produtos=[], cocktails=cocktails) == 1

def test_contar_coqueteis_possiveis_missing_ingredients():
    cocktails = [
        {"nome": "Caipirinha", "ingredientes": [{"produto_id": 1}, {"produto_id": 2}]}
    ]
    # No products
    assert contar_coqueteis_possiveis(produtos=[], cocktails=cocktails) == 0

    # Missing some products
    produtos = [{"id": 1}]
    assert contar_coqueteis_possiveis(produtos=produtos, cocktails=cocktails) == 0

def test_contar_coqueteis_possiveis_all_ingredients_available():
    cocktails = [
        {"nome": "Caipirinha", "ingredientes": [{"produto_id": 1}, {"produto_id": 2}]}
    ]
    produtos = [{"id": 1}, {"id": 2}, {"id": 3}]
    assert contar_coqueteis_possiveis(produtos=produtos, cocktails=cocktails) == 1

def test_contar_coqueteis_possiveis_multiple_cocktails():
    cocktails = [
        {"nome": "Caipirinha", "ingredientes": [{"produto_id": 1}, {"produto_id": 2}]},
        {"nome": "Mojito", "ingredientes": [{"produto_id": 3}, {"produto_id": 4}]},
        {"nome": "Gin Tonic", "ingredientes": [{"produto_id": 5}, {"produto_id": 6}]}
    ]
    produtos = [{"id": 1}, {"id": 2}, {"id": 5}, {"id": 6}]
    # Caipirinha and Gin Tonic are possible, Mojito is not
    assert contar_coqueteis_possiveis(produtos=produtos, cocktails=cocktails) == 2
