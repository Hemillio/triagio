import pytest

from app import create_app
from app.clientes.models import Cliente, Veiculo
from app.extensions import db


@pytest.fixture()
def app():
    aplicacao = create_app({
        "TESTING": True,
        "SECRET_KEY": "somente-testes",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with aplicacao.app_context():
        db.create_all()
        yield aplicacao
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def exemplo(**alteracoes):
    dados = {
        "nome": "Pessoa fictícia",
        "telefone": "000000000",
        "placa": "ABC1D23",
        "modelo": "Veículo exemplo",
        "ano": "2020",
    }
    dados.update(alteracoes)
    return dados


def test_formulario_de_cliente_abre(client):
    resposta = client.get("/clientes/novo")
    assert resposta.status_code == 200
    assert b"Cadastrar cliente" in resposta.data


def test_cadastro_cria_cliente_e_veiculo_associado(app, client):
    resposta = client.post("/clientes/novo", data=exemplo())
    assert resposta.status_code == 303
    with app.app_context():
        cliente = db.session.query(Cliente).one()
        veiculo = db.session.query(Veiculo).one()
        assert veiculo.cliente_id == cliente.id
        assert veiculo.placa == "ABC1D23"
        assert veiculo.modelo == "Veículo exemplo"
        assert veiculo.ano == 2020
        assert veiculo.ativo is True


def test_placa_duplicada_nao_cria_outro_cliente(app, client):
    assert client.post("/clientes/novo", data=exemplo()).status_code == 303
    resposta = client.post(
        "/clientes/novo",
        data=exemplo(nome="Outra pessoa", placa="abc-1d23"),
    )
    assert resposta.status_code == 422
    assert "Placa já cadastrada" in resposta.get_data(as_text=True)
    with app.app_context():
        assert db.session.query(Cliente).count() == 1
        assert db.session.query(Veiculo).count() == 1


def test_cadastro_invalido_nao_grava_dados(app, client):
    resposta = client.post("/clientes/novo", data=exemplo(ano="invalido"))
    assert resposta.status_code == 422
    with app.app_context():
        assert db.session.query(Cliente).count() == 0
        assert db.session.query(Veiculo).count() == 0


def test_adicionar_veiculo_a_cliente_existente(app, client):
    with app.app_context():
        pessoa = Cliente(nome="Cliente de teste", telefone="", ativo=True)
        db.session.add(pessoa)
        db.session.commit()
        cliente_id = pessoa.id

    resposta = client.post("/veiculos/novo", data={
        "cliente_id": str(cliente_id), "placa": "AAA1A11",
        "modelo": "Segundo carro", "ano": "2021",
    })
    assert resposta.status_code == 303
    with app.app_context():
        veiculo = db.session.query(Veiculo).one()
        assert veiculo.cliente_id == cliente_id


def test_busca_localiza_por_placa_sem_hifen(client):
    assert client.post("/clientes/novo", data=exemplo()).status_code == 303
    resposta = client.get("/veiculos?placa=abc-1d23")
    assert resposta.status_code == 200
    assert b"ABC1D23" in resposta.data


def test_veiculo_inativo_nao_pode_receber_novo_cadastro_duplicado(app, client):
    assert client.post("/clientes/novo", data=exemplo()).status_code == 303
    with app.app_context():
        veiculo = db.session.query(Veiculo).one()
        veiculo.ativo = False
        db.session.commit()
    resposta = client.post("/clientes/novo", data=exemplo(nome="Outra pessoa"))
    assert resposta.status_code == 422
    with app.app_context():
        assert db.session.query(Veiculo).count() == 1
