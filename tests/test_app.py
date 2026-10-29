from app import create_app
from app.extensions import db


def test_inicio_abre_sem_modulos_de_negocio():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "apenas-teste",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    resposta = app.test_client().get("/")
    assert resposta.status_code == 200
    assert b"Triagio" in resposta.data



def test_configuracao_de_teste_altera_banco():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        assert db.engine.url.get_backend_name() == "sqlite"
        assert db.engine.url.database == ":memory:"