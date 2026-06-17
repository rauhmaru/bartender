import os
import tempfile
import pytest

import app

@pytest.fixture
def client():
    db_fd, temp_db_path = tempfile.mkstemp()
    # override DB_PATH in app module
    app.DB_PATH = temp_db_path

    app.app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-key"
    })

    with app.app.test_client() as client:
        with app.app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(temp_db_path)

def test_index_redirects(client):
    """Test that the index route redirects to the /cadastrar route."""
    rv = client.get("/")
    assert rv.status_code == 302
    assert "/cadastrar" in rv.location

def test_cadastrar_get(client):
    """Test that the /cadastrar route returns the form correctly."""
    rv = client.get("/cadastrar")
    assert rv.status_code == 200
    assert b"Cadastrar" in rv.data

def test_cadastrar_post(client):
    """Test that submitting the /cadastrar form works correctly."""
    # First, add the product type so it validates
    client.post("/tipos", data={"nome": "Test Type"})

    rv = client.post("/cadastrar", data={
        "produto": "Test Product",
        "tipo": "Test Type",
        "volume_ml": "1000"
    }, follow_redirects=True)

    assert rv.status_code == 200
    assert b"Produto cadastrado com sucesso!" in rv.data

def test_visualizar(client):
    """Test that the /visualizar route lists the added products."""
    client.post("/tipos", data={"nome": "Test Type"})
    client.post("/cadastrar", data={
        "produto": "Test Product",
        "tipo": "Test Type",
        "volume_ml": "1000"
    }, follow_redirects=True)

    rv = client.get("/visualizar")
    assert rv.status_code == 200
    assert b"Test Product" in rv.data
    assert b"Test Type" in rv.data
    assert b"1000" in rv.data

def test_listar_produtos_empty(client):
    """Test the /visualizar route when there are no products."""
    rv = client.get("/visualizar")
    assert rv.status_code == 200
    assert b"Nenhum produto" in rv.data or b"Nenhum" in rv.data
