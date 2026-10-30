from pathlib import Path
from uuid import uuid4

from flask import abort, current_app, redirect, send_from_directory, url_for
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.portal import bp
from app.portal.models import Laudo
from app.portal.pdf import criar_pdf_laudo
from app.portal.routes import resposta_sem_cache
from app.portal.servicos import consultar_token
from app.vistorias.models import Vistoria
from app.vistorias.servicos import agora_utc_iso


def _diretorio_laudos():
    return Path(current_app.instance_path) / "laudos"


@bp.post("/portal/vistorias/<int:vistoria_id>/laudo")
def gerar_laudo(vistoria_id):
    vistoria = db.session.get(Vistoria, vistoria_id)
    if vistoria is None:
        abort(404)

    anterior = db.session.query(Laudo).filter_by(vistoria_id=vistoria.id).first()
    if anterior is not None:
        if vistoria.status != "LaudoDisponivel":
            return "Inconsistência entre laudo e estado da vistoria.", 409
        return redirect(url_for("portal.gerenciar_acesso", vistoria_id=vistoria.id), code=303)

    if vistoria.status != "Finalizada" or not vistoria.finalizada_em:
        return "Somente uma vistoria finalizada pode gerar laudo.", 422

    nome_pdf = f"vistoria-{vistoria.id}-{uuid4().hex}.pdf"
    caminho = _diretorio_laudos() / nome_pdf
    try:
        criar_pdf_laudo(vistoria, caminho)
        registro = Laudo(
            vistoria_id=vistoria.id,
            emitido_em=agora_utc_iso(),
            caminho_arquivo=f"laudos/{nome_pdf}",
        )
        db.session.add(registro)
        vistoria.status = "LaudoDisponivel"
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        caminho.unlink(missing_ok=True)
        return "Laudo já gerado em outra solicitação. Atualize a página.", 409
    except Exception:
        db.session.rollback()
        caminho.unlink(missing_ok=True)
        raise

    return redirect(url_for("portal.gerenciar_acesso", vistoria_id=vistoria.id), code=303)


@bp.get("/acompanhar/<token>/laudo.pdf")
def baixar_laudo(token):
    registro_token = consultar_token(token)
    if registro_token is None:
        abort(404)

    vistoria = registro_token.vistoria
    if vistoria.status != "LaudoDisponivel":
        abort(404)

    registro_laudo = db.session.query(Laudo).filter_by(vistoria_id=vistoria.id).first()
    if registro_laudo is None:
        abort(404)

    nome = Path(registro_laudo.caminho_arquivo).name
    if registro_laudo.caminho_arquivo != f"laudos/{nome}":
        abort(404)

    resposta = send_from_directory(
        _diretorio_laudos(),
        nome,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"laudo-vistoria-{vistoria.id}.pdf",
    )
    return resposta_sem_cache(resposta)
