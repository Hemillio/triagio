from flask import current_app, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.agendamentos import bp
from app.agendamentos.models import Agendamento
from app.agendamentos.servicos import (
    HorarioInvalido,
    converter_horario_para_utc,
    formatar_horario_local,
)
from app.clientes.models import Veiculo
from app.extensions import db


def _veiculos_ativos():
    return db.session.query(Veiculo).filter_by(
        ativo=True
    ).order_by(Veiculo.placa).all()


@bp.get("")
@bp.get("/")
def lista():
    agendamentos = db.session.query(Agendamento).order_by(
        Agendamento.data_hora
    ).all()

    fuso = current_app.config["TRIAGIO_TIMEZONE"]

    return render_template(
        "agendamentos/lista.html",
        agendamentos=agendamentos,
        formatar_hora=lambda data: formatar_horario_local(data, fuso),
    )


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    erro = None
    valores = {"veiculo_id": "", "data_hora": ""}
    veiculos = _veiculos_ativos()

    if request.method == "POST":
        valores = {
            "veiculo_id": request.form.get("veiculo_id", "").strip(),
            "data_hora": request.form.get("data_hora", "").strip(),
        }

        veiculo = None

        if not valores["veiculo_id"].isdecimal():
            erro = "Selecione um veículo válido."
        else:
            veiculo = db.session.get(
                Veiculo, int(valores["veiculo_id"])
            )

            if veiculo is None or not veiculo.ativo:
                erro = "Veículo inexistente ou inativo."

        if erro is None:
            try:
                data_utc = converter_horario_para_utc(
                    valores["data_hora"],
                    current_app.config["TRIAGIO_TIMEZONE"]
                )
            except HorarioInvalido as exc:
                erro = str(exc)

        if erro is None:
            agendamento = Agendamento(
                veiculo_id=veiculo.id,
                data_hora=data_utc,
                status="Agendado"
            )

            db.session.add(agendamento)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                erro = "Não foi possível salvar o agendamento. Verifique os dados."
            else:
                return redirect(
                    url_for("agendamentos.lista"),
                    code=303
                )

    return render_template(
        "agendamentos/novo.html",
        veiculos=veiculos,
        erro=erro,
        valores=valores,
    ), (422 if erro else 200)
