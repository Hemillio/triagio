
from datetime import datetime, timezone

from app import create_app
from app.clientes.models import Cliente, Veiculo
from app.extensions import db
from app.vistorias.models import Vistoria


def criar_app_teste():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "teste",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
    return app


def criar_veiculo():
    cliente = Cliente(nome="Cliente Teste", telefone="11999999999", ativo=True)
    db.session.add(cliente)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        placa="ABC1D23",
        modelo="Carro Teste",
        ano=2022,
        ativo=True,
    )
    db.session.add(veiculo)
    db.session.commit()
    return veiculo


def test_historico_vazio():
    app = criar_app_teste()
    with app.app_context():
        veiculo = criar_veiculo()
        veiculo_id = veiculo.id

    resposta = app.test_client().get(f"/veiculos/{veiculo_id}/historico")

    assert resposta.status_code == 200
    assert b"Nenhuma vistoria encontrada" in resposta.data


def test_historico_veiculo_inexistente():
    app = criar_app_teste()

    resposta = app.test_client().get("/veiculos/999/historico")

    assert resposta.status_code == 404


def test_historico_lista_vistorias():
    app = criar_app_teste()
    with app.app_context():
        veiculo = criar_veiculo()
        veiculo_id = veiculo.id

        antiga = Vistoria(
            veiculo_id=veiculo_id,
            iniciada_em="2026-01-10T10:00:00+00:00",
            status="Finalizada",
        )
        recente = Vistoria(
            veiculo_id=veiculo_id,
            iniciada_em="2026-02-10T10:00:00+00:00",
            status="EmPreenchimento",
        )
        db.session.add_all([antiga, recente])
        db.session.commit()

    resposta = app.test_client().get(f"/veiculos/{veiculo_id}/historico")

    assert resposta.status_code == 200
    assert resposta.data.index(b"10/02/2026 07:00") < resposta.data.index(b"10/01/2026 07:00")
    assert b"EmPreenchimento" in resposta.data
    assert b"Finalizada" in resposta.data
