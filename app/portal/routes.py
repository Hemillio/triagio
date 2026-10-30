from flask import abort, make_response, redirect, render_template, url_for

from app.extensions import db
from app.portal import bp
from app.portal.models import TokenAcesso
from app.portal.servicos import consultar_token, obter_ou_criar_token
from app.vistorias.models import Vistoria


def resposta_sem_cache(resposta):
    resposta.headers["Cache-Control"] = "private, no-store"
    resposta.headers["Referrer-Policy"] = "no-referrer"
    resposta.headers["X-Robots-Tag"] = "noindex, nofollow"
    return resposta


@bp.get("/portal/vistorias/<int:vistoria_id>/acesso")
def gerenciar_acesso(vistoria_id):
    vistoria = db.session.get(Vistoria, vistoria_id)
    if vistoria is None:
        abort(404)

    registro = db.session.query(TokenAcesso).filter_by(vistoria_id=vistoria.id).first()
    link = (
        url_for("portal.acompanhar", token=registro.token, _external=True)
        if registro is not None
        else None
    )
    resposta = make_response(
        render_template(
            "portal/gerenciar.html",
            vistoria=vistoria,
            registro=registro,
            link=link,
        )
    )
    return resposta_sem_cache(resposta)


@bp.post("/portal/vistorias/<int:vistoria_id>/token")
def gerar_token(vistoria_id):
    vistoria = db.session.get(Vistoria, vistoria_id)
    if vistoria is None:
        abort(404)

    obter_ou_criar_token(vistoria)
    return redirect(url_for("portal.gerenciar_acesso", vistoria_id=vistoria.id), code=303)


@bp.get("/acompanhar/<token>")
def acompanhar(token):
    registro = consultar_token(token)
    if registro is None:
        abort(404)

    resposta = make_response(
        render_template(
            "portal/acompanhamento.html",
            vistoria=registro.vistoria,
            registro=registro,
        )
    )
    return resposta_sem_cache(resposta)
