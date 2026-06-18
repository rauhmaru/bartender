from app import _validar, MAX_PRODUTO, MAX_TIPO, MAX_VOLUME

def test_validar_happy_path():
    assert _validar("Produto 1", "Tipo A", "100") is None
    assert _validar("Produto 2", "Tipo B", "500", tipos_validos=["Tipo B", "Tipo C"]) is None

def test_validar_missing_fields():
    assert _validar("", "Tipo A", "100") == "O campo 'Produto' é obrigatório."
    assert _validar(None, "Tipo A", "100") == "O campo 'Produto' é obrigatório."
    assert _validar("Produto 1", "", "100") == "O campo 'Tipo' é obrigatório."
    assert _validar("Produto 1", None, "100") == "O campo 'Tipo' é obrigatório."
    assert _validar("Produto 1", "Tipo A", "") == "O campo 'Volume (ml)' é obrigatório."
    assert _validar("Produto 1", "Tipo A", None) == "O campo 'Volume (ml)' é obrigatório."

def test_validar_length_validation():
    long_produto = "a" * (MAX_PRODUTO + 1)
    assert _validar(long_produto, "Tipo A", "100") == f"'Produto' deve ter no máximo {MAX_PRODUTO} caracteres."

    long_tipo = "a" * (MAX_TIPO + 1)
    assert _validar("Produto 1", long_tipo, "100") == f"'Tipo' deve ter no máximo {MAX_TIPO} caracteres."

def test_validar_invalid_tipo():
    assert _validar("Produto 1", "Tipo A", "100", tipos_validos=["Tipo B", "Tipo C"]) == "Selecione um tipo de produto válido."

def test_validar_non_digit_volume():
    assert _validar("Produto 1", "Tipo A", "abc") == "'Volume (ml)' deve ser um número inteiro."
    assert _validar("Produto 1", "Tipo A", "10.5") == "'Volume (ml)' deve ser um número inteiro."
    assert _validar("Produto 1", "Tipo A", "-10") == "'Volume (ml)' deve ser um número inteiro."

def test_validar_volume_boundaries():
    volume_acima = str(MAX_VOLUME + 1)
    assert _validar("Produto 1", "Tipo A", volume_acima) == f"'Volume (ml)' deve estar entre 0 e {MAX_VOLUME}."
import pytest
from app import _validar_cocktail, MAX_NOME, MAX_TACARIA, MAX_QUANTIDADE

@pytest.fixture
def base_produtos():
    return [
        {"id": 1, "produto": "Gin"},
        {"id": 2, "produto": "Tônica"},
        {"id": 3, "produto": "Limão"}
    ]

def test_validar_cocktail_happy_path(base_produtos):
    nome = "Gin Tônica"
    tacaria = "Taça de Gin"
    receita = "Misturar tudo com gelo"
    produto_ids = ["1", "2"]
    quantidades = ["50", "150.5"]

    error, ingredientes = _validar_cocktail(nome, tacaria, receita, produto_ids, quantidades, base_produtos)

    assert error is None
    assert ingredientes == [(1, 50.0), (2, 150.5)]

def test_validar_cocktail_empty_fields(base_produtos):
    # Empty nome
    error, _ = _validar_cocktail("", "Taça", "Receita", ["1"], ["50"], base_produtos)
    assert error == "O campo 'Nome do coquetel' é obrigatório."

    # Empty tacaria
    error, _ = _validar_cocktail("Nome", "", "Receita", ["1"], ["50"], base_produtos)
    assert error == "O campo 'Taçaria' é obrigatório."

    # Empty receita
    error, _ = _validar_cocktail("Nome", "Taça", "", ["1"], ["50"], base_produtos)
    assert error == "O campo 'Receita' é obrigatório."

def test_validar_cocktail_exceed_limits(base_produtos):
    # Exceed nome length
    long_nome = "A" * (MAX_NOME + 1)
    error, _ = _validar_cocktail(long_nome, "Taça", "Receita", ["1"], ["50"], base_produtos)
    assert error == f"'Nome do coquetel' deve ter no máximo {MAX_NOME} caracteres."

    # Exceed tacaria length
    long_tacaria = "A" * (MAX_TACARIA + 1)
    error, _ = _validar_cocktail("Nome", long_tacaria, "Receita", ["1"], ["50"], base_produtos)
    assert error == f"'Taçaria' deve ter no máximo {MAX_TACARIA} caracteres."

def test_validar_cocktail_ingredients(base_produtos):
    # Empty pairs being skipped
    error, ingredientes = _validar_cocktail("Nome", "Taça", "Receita", ["", "1"], ["", "50"], base_produtos)
    assert error is None
    assert ingredientes == [(1, 50.0)]

    # Missing product ID
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["", "1"], ["50", "50"], base_produtos)
    assert error == "Selecione o produto de todos os ingredientes."

    # Invalid product ID string
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["abc"], ["50"], base_produtos)
    assert error == "Ingrediente inválido."

    # Product ID not in produtos
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["99"], ["50"], base_produtos)
    assert error == "Ingrediente inválido: produto não cadastrado."

    # Missing quantity
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["1"], [""], base_produtos)
    assert error == "Informe a quantidade (ml) de cada ingrediente."

    # Invalid quantity string
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["1"], ["abc"], base_produtos)
    assert error == "'Quantidade' deve ser um número (ml)."

    # Quantity <= 0
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["1"], ["0"], base_produtos)
    assert error == f"'Quantidade' deve ser maior que 0 e ate {int(MAX_QUANTIDADE)}."

    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["1"], ["-50"], base_produtos)
    assert error == f"'Quantidade' deve ser maior que 0 e ate {int(MAX_QUANTIDADE)}."

    # Quantity > MAX_QUANTIDADE
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["1"], [str(MAX_QUANTIDADE + 1)], base_produtos)
    assert error == f"'Quantidade' deve ser maior que 0 e ate {int(MAX_QUANTIDADE)}."

    # Empty ingredients overall
    error, _ = _validar_cocktail("Nome", "Taça", "Receita", ["", ""], ["", ""], base_produtos)
    assert error == "Adicione pelo menos um ingrediente."

    # Handle comma decimals
    error, ingredientes = _validar_cocktail("Nome", "Taça", "Receita", ["1"], ["50,5"], base_produtos)
    assert error is None
    assert ingredientes == [(1, 50.5)]
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
