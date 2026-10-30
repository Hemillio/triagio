from pathlib import Path

import pytest

from app import create_app
from app.clientes.models import Cliente, Veiculo
from app.extensions import db
from app.portal.models import Laudo, TokenAcesso
from app.vistorias.models import Avaria, Vistoria


@pytest.fixture()
def app(tmp_path):
    aplicacao = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "somente-testes-joao",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    aplicacao.instance_path = str(tmp_path / "instance")
    with aplicacao.app_context():
        db.create_all()
        yield aplicacao
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def vistoria_id(app):
    with app.app_context():
        cliente = Cliente(nome="Pessoa Fictícia", telefone="0000000", ativo=True)
        db.session.add(cliente)
        db.session.flush()
        veiculo = Veiculo(
            cliente_id=cliente.id,
            placa="ABC1D23",
            modelo="Modelo de teste",
            ano=2020,
            ativo=True,
        )
        db.session.add(veiculo)
        db.session.flush()
        vistoria = Vistoria(
            veiculo_id=veiculo.id,
            iniciada_em="2026-10-28T10:00:00+00:00",
            status="EmPreenchimento",
            nivel_combustivel="1/2",
            observacoes="Sem ressalvas na entrada.",
        )
        db.session.add(vistoria)
        db.session.flush()
        db.session.add(
            Avaria(vistoria_id=vistoria.id, regiao="Frente", descricao="Risco leve")
        )
        db.session.commit()
        return vistoria.id


def criar_token(client, identificador):
    resposta = client.post(f"/portal/vistorias/{identificador}/token")
    assert resposta.status_code == 303
    return resposta


def token_do_banco(app, identificador):
    with app.app_context():
        registro = db.session.query(TokenAcesso).filter_by(vistoria_id=identificador).one()
        return registro.token


def test_token_unico_idempotente_e_aleatorio(app, client, vistoria_id):
    criar_token(client, vistoria_id)
    token_inicial = token_do_banco(app, vistoria_id)
    assert len(token_inicial) >= 40
    assert token_inicial != str(vistoria_id)
    criar_token(client, vistoria_id)
    with app.app_context():
        assert (
            db.session.query(TokenAcesso).filter_by(vistoria_id=vistoria_id).count() == 1
        )
        assert token_do_banco(app, vistoria_id) == token_inicial


def test_token_invalido_nao_revela_dados(client):
    resposta = client.get("/acompanhar/token-inexistente")
    assert resposta.status_code == 404
    assert b"Pessoa" not in resposta.data
    resposta_pdf = client.get("/acompanhar/token-inexistente/laudo.pdf")
    assert resposta_pdf.status_code == 404


def test_acompanhamento_exibe_status_sem_dados_pessoais(app, client, vistoria_id):
    criar_token(client, vistoria_id)
    token = token_do_banco(app, vistoria_id)
    resposta = client.get(f"/acompanhar/{token}")
    assert resposta.status_code == 200
    assert "Em preenchimento" in resposta.get_data(as_text=True)
    assert "Pessoa Fictícia" not in resposta.get_data(as_text=True)
    assert "0000000" not in resposta.get_data(as_text=True)
    assert resposta.headers["Cache-Control"] == "private, no-store"
    assert resposta.headers["Referrer-Policy"] == "no-referrer"


def test_rascunho_nao_gera_laudo(app, client, vistoria_id):
    resposta = client.post(f"/portal/vistorias/{vistoria_id}/laudo")
    assert resposta.status_code == 422
    with app.app_context():
        assert db.session.query(Laudo).filter_by(vistoria_id=vistoria_id).count() == 0
        assert db.session.get(Vistoria, vistoria_id).status == "EmPreenchimento"


def test_laudo_finalizado_gera_pdf_e_muda_estado(app, client, vistoria_id):
    criar_token(client, vistoria_id)
    assert client.post(f"/vistorias/{vistoria_id}/finalizar").status_code == 303
    resposta = client.post(f"/portal/vistorias/{vistoria_id}/laudo")
    assert resposta.status_code == 303

    with app.app_context():
        registro = db.session.query(Laudo).filter_by(vistoria_id=vistoria_id).one()
        vistoria = db.session.get(Vistoria, vistoria_id)
        assert vistoria.status == "LaudoDisponivel"
        assert vistoria.finalizada_em is not None
        assert registro.emitido_em.endswith("+00:00")
        arquivo = Path(app.instance_path) / registro.caminho_arquivo
        assert arquivo.exists()
        assert arquivo.read_bytes().startswith(b"%PDF-")

    token = token_do_banco(app, vistoria_id)
    pagina = client.get(f"/acompanhar/{token}")
    assert pagina.status_code == 200
    assert "Laudo disponível" in pagina.get_data(as_text=True)
    assert f"/acompanhar/{token}/laudo.pdf" in pagina.get_data(as_text=True)

    pdf = client.get(f"/acompanhar/{token}/laudo.pdf")
    assert pdf.status_code == 200
    assert pdf.mimetype == "application/pdf"
    assert pdf.data.startswith(b"%PDF-")
    assert pdf.headers["Cache-Control"] == "private, no-store"


def test_geracao_repetida_nao_duplica_laudo(app, client, vistoria_id):
    assert client.post(f"/vistorias/{vistoria_id}/finalizar").status_code == 303
    assert client.post(f"/portal/vistorias/{vistoria_id}/laudo").status_code == 303
    with app.app_context():
        primeiro = db.session.query(Laudo).filter_by(vistoria_id=vistoria_id).one()
        caminho_original = primeiro.caminho_arquivo
    assert client.post(f"/portal/vistorias/{vistoria_id}/laudo").status_code == 303
    with app.app_context():
        registros = db.session.query(Laudo).filter_by(vistoria_id=vistoria_id).all()
        assert len(registros) == 1
        assert registros[0].caminho_arquivo == caminho_original


def test_pdf_nao_disponivel_antes_de_emissao(app, client, vistoria_id):
    criar_token(client, vistoria_id)
    token = token_do_banco(app, vistoria_id)
    assert client.get(f"/acompanhar/{token}/laudo.pdf").status_code == 404
    assert client.post(f"/vistorias/{vistoria_id}/finalizar").status_code == 303
    assert client.get(f"/acompanhar/{token}/laudo.pdf").status_code == 404


def test_token_diferente_para_outra_vistoria(app, client, vistoria_id):
    with app.app_context():
        original = db.session.get(Vistoria, vistoria_id)
        outra = Vistoria(
            veiculo_id=original.veiculo_id,
            iniciada_em="2026-10-28T11:00:00+00:00",
            status="EmPreenchimento",
            nivel_combustivel="cheio",
            observacoes="",
        )
        db.session.add(outra)
        db.session.commit()
        outro_id = outra.id
    criar_token(client, vistoria_id)
    criar_token(client, outro_id)
    assert token_do_banco(app, vistoria_id) != token_do_banco(app, outro_id)
