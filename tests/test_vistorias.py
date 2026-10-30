
from io import BytesIO

import pytest
from PIL import Image

from app import create_app
from app.clientes.models import Cliente, Veiculo
from app.extensions import db
from app.vistorias.models import Avaria, Foto, Pertence, Vistoria


@pytest.fixture()
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "chave-apenas-de-testes",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    app.instance_path = str(tmp_path / "instance")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def veiculo_id(app):
    with app.app_context():
        cliente = Cliente(nome="Pessoa Exemplo", telefone="000000000", ativo=True)
        db.session.add(cliente)
        db.session.flush()
        veiculo = Veiculo(
            cliente_id=cliente.id, placa="ABC1D23", modelo="Modelo fictício",
            ano=2020, ativo=True,
        )
        db.session.add(veiculo)
        db.session.commit()
        return veiculo.id


def criar_vistoria(client, veiculo_id):
    resposta = client.post(f"/vistorias/iniciar/{veiculo_id}")
    assert resposta.status_code == 303
    return int(resposta.headers["Location"].rstrip("/").split("/")[-1])


def imagem_png():
    memoria = BytesIO()
    Image.new("RGB", (2, 2), "white").save(memoria, format="PNG")
    memoria.seek(0)
    return memoria


def test_criacao_e_associacao_com_veiculo(app, client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    with app.app_context():
        vistoria = db.session.get(Vistoria, id_v)
        assert vistoria.veiculo_id == veiculo_id
        assert vistoria.status == "EmPreenchimento"
        assert "+00:00" in vistoria.iniciada_em


def test_checklist_salva_avaria_pertence_e_combustivel(app, client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    resposta = client.post(f"/vistorias/{id_v}", data={
        "nivel_combustivel": "1/2",
        "observacoes": "Acompanhamento de demonstração",
        "avarias": "Frente | risco no para-choque",
        "pertences": "Triângulo\nMacaco",
    })
    assert resposta.status_code == 303
    with app.app_context():
        vistoria = db.session.get(Vistoria, id_v)
        assert vistoria.nivel_combustivel == "1/2"
        assert len(vistoria.avarias) == 1
        assert vistoria.avarias[0].regiao == "Frente"
        assert len(vistoria.pertences) == 2


def test_avaria_invalida_nao_persiste(app, client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    resposta = client.post(f"/vistorias/{id_v}", data={
        "nivel_combustivel": "cheio", "avarias": "sem separador",
        "pertences": "", "observacoes": "",
    })
    assert resposta.status_code == 422
    with app.app_context():
        assert db.session.query(Avaria).filter_by(vistoria_id=id_v).count() == 0


def test_finalizar_bloqueia_edicao_e_registra_data(app, client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    assert client.post(f"/vistorias/{id_v}/finalizar").status_code == 303
    assert client.post(f"/vistorias/{id_v}", data={
        "nivel_combustivel": "cheio", "observacoes": "Mudança indevida",
        "avarias": "", "pertences": "",
    }).status_code == 422
    with app.app_context():
        vistoria = db.session.get(Vistoria, id_v)
        assert vistoria.status == "Finalizada"
        assert vistoria.finalizada_em is not None
        assert "+00:00" in vistoria.finalizada_em


def test_foto_valida_e_limite_quatro(app, client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    for _ in range(4):
        resposta = client.post(
            f"/vistorias/{id_v}/fotos",
            data={"foto": (imagem_png(), "imagem.png")},
            content_type="multipart/form-data",
        )
        assert resposta.status_code == 303
    resposta = client.post(
        f"/vistorias/{id_v}/fotos",
        data={"foto": (imagem_png(), "quinta.png")},
        content_type="multipart/form-data",
    )
    assert resposta.status_code == 422
    with app.app_context():
        assert db.session.query(Foto).filter_by(vistoria_id=id_v).count() == 4


def test_foto_maior_que_3_mib_e_rejeitada(client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    resposta = client.post(
        f"/vistorias/{id_v}/fotos",
        data={"foto": (BytesIO(b"x" * (3 * 1024 * 1024 + 1)), "grande.png")},
        content_type="multipart/form-data",
    )
    assert resposta.status_code == 422
    assert b"3 MB" in resposta.data


def test_arquivo_falso_e_rejeitado(client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    resposta = client.post(
        f"/vistorias/{id_v}/fotos",
        data={"foto": (BytesIO(b"texto que nao e imagem"), "falso.jpg")},
        content_type="multipart/form-data",
    )
    assert resposta.status_code == 422


def test_foto_nao_pode_ser_adicionada_apos_finalizacao(client, veiculo_id):
    id_v = criar_vistoria(client, veiculo_id)
    client.post(f"/vistorias/{id_v}/finalizar")
    resposta = client.post(
        f"/vistorias/{id_v}/fotos",
        data={"foto": (imagem_png(), "foto.png")},
        content_type="multipart/form-data",
    )
    assert resposta.status_code == 422
