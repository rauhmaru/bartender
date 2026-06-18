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
