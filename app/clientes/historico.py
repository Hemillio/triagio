
from flask import abort, current_app, render_template
from sqlalchemy import select

from app.clientes import bp
from app.clientes.models import Veiculo
from app.clientes.servicos import formatar_data_local
from app.extensions import db
from app.vistorias.models import Vistoria


@bp.get("/veiculos/<int:veiculo_id>/historico")
def historico(veiculo_id):
    veiculo = db.session.get(Veiculo, veiculo_id)

    if veiculo is None:
        abort(404)

    vistorias = db.session.scalars(
        select(Vistoria)
        .where(Vistoria.veiculo_id == veiculo_id)
        .order_by(Vistoria.iniciada_em.desc(), Vistoria.id.desc())
    ).all()

    fuso = current_app.config.get(
        "TRIAGIO_TIMEZONE",
        "America/Araguaina",
    )

    return render_template(
        "clientes/historico.html",
        veiculo=veiculo,
        vistorias=vistorias,
        formatar_data=lambda valor: formatar_data_local(valor, fuso),
    )
