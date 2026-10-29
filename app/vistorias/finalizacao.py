
from flask import abort, redirect, url_for

from app.extensions import db
from app.vistorias import bp
from app.vistorias.models import Vistoria
from app.vistorias.servicos import agora_utc_iso


@bp.post("/<int:vistoria_id>/finalizar")
def finalizar(vistoria_id):
    vistoria = db.session.get(Vistoria, vistoria_id)
    if vistoria is None:
        abort(404)
    if vistoria.status != "EmPreenchimento":
        return "Esta vistoria já foi finalizada e não pode ser finalizada novamente.", 422

    vistoria.status = "Finalizada"
    vistoria.finalizada_em = agora_utc_iso()
    db.session.commit()
    return redirect(url_for("vistorias.detalhe", vistoria_id=vistoria.id), code=303)
