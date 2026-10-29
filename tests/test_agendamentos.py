import pytest

from app import create_app
from app.agendamentos.models import Agendamento
from app.clientes.models import Cliente, Veiculo
from app.extensions import db


@pytest.fixture
def app_teste():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "chave-apenas-para-testes",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def cliente_http(app_teste):
    return app_teste.test_client()


@pytest.fixture
def veiculos(app_teste):
    with app_teste.app_context():
        cliente_a = Cliente(nome="Cliente Teste A")
        cliente_b = Cliente(nome="Cliente Teste B")

        db.session.add_all([cliente_a, cliente_b])
        db.session.flush()

        corolla = Veiculo(
            cliente_id=cliente_a.id,
            placa="AAA1A11",
            modelo="Corolla",
            ano=2020,
            ativo=True,
        )

        civic = Veiculo(
            cliente_id=cliente_b.id,
            placa="BBB2B22",
            modelo="Civic",
            ano=2022,
            ativo=True,
        )

        db.session.add_all([corolla, civic])
        db.session.commit()

        return corolla.id, civic.id


def test_lista_inicial_vazia(cliente_http):
    resposta = cliente_http.get("/agendamentos")

    assert resposta.status_code == 200
    assert "Nenhuma recepção agendada" in resposta.get_data(
        as_text=True
    )


def test_criar_agendamento_valido(
    app_teste, cliente_http, veiculos
):
    resposta = cliente_http.post(
        "/agendamentos/novo",
        data={
            "veiculo_id": str(veiculos[0]),
            "data_hora": "2026-11-03T14:00",
        },
    )

    assert resposta.status_code == 303

    with app_teste.app_context():
        agendamento = db.session.query(Agendamento).one()

        assert agendamento.veiculo_id == veiculos[0]
        assert agendamento.status == "Agendado"
        assert agendamento.data_hora == "2026-11-03T17:00+00:00"


def test_dois_veiculos_no_mesmo_horario(
    app_teste, cliente_http, veiculos
):
    for veiculo_id in veiculos:
        resposta = cliente_http.post(
            "/agendamentos/novo",
            data={
                "veiculo_id": str(veiculo_id),
                "data_hora": "2026-11-03T14:00",
            },
        )

        assert resposta.status_code == 303

    with app_teste.app_context():
        agendamentos = db.session.query(Agendamento).all()

        assert len(agendamentos) == 2
        assert agendamentos[0].data_hora == agendamentos[1].data_hora
        assert agendamentos[0].veiculo_id != agendamentos[1].veiculo_id


def test_veiculo_inexistente(
    app_teste, cliente_http
):
    resposta = cliente_http.post(
        "/agendamentos/novo",
        data={
            "veiculo_id": "99999",
            "data_hora": "2026-11-03T14:00",
        },
    )

    assert resposta.status_code == 422

    with app_teste.app_context():
        assert db.session.query(Agendamento).count() == 0


def test_horario_invalido(
    app_teste, cliente_http, veiculos
):
    resposta = cliente_http.post(
        "/agendamentos/novo",
        data={
            "veiculo_id": str(veiculos[0]),
            "data_hora": "data-invalida",
        },
    )

    assert resposta.status_code == 422

    with app_teste.app_context():
        assert db.session.query(Agendamento).count() == 0
