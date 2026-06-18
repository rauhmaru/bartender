import pytest
from app import _validar_cocktail, MAX_RECEITA

def test_validar_cocktail_receita():
    nome = "Test Cocktail"
    tacaria = "Taça Teste"
    produtos = [{"id": 1}]
    produto_ids = ["1"]
    quantidades = ["50"]

    # Valid receita
    receita_valid = "A" * MAX_RECEITA
    error, ing = _validar_cocktail(nome, tacaria, receita_valid, produto_ids, quantidades, produtos)
    assert error is None

    # Invalid receita (too long)
    receita_invalid = "A" * (MAX_RECEITA + 1)
    error, ing = _validar_cocktail(nome, tacaria, receita_invalid, produto_ids, quantidades, produtos)
    assert error == f"'Receita' deve ter no máximo {MAX_RECEITA} caracteres."
