
from flask import abort, redirect, render_template, request, url_for

from app.clientes.models import Veiculo
from app.extensions import db
from app.vistorias import bp
from app.vistorias.models import Avaria, Pertence, Vistoria
from app.vistorias.servicos import (
    COMBUSTIVEIS,
    agora_utc_iso,
    interpretar_avarias,
    interpretar_pertences,
)


def _obter_vistoria(vistoria_id):
    vistoria = db.session.get(Vistoria, vistoria_id)
    if vistoria is None:
        abort(404)
    return vistoria


def _campos(vistoria, valores=None):
    if valores is not None:
        return {
            "nivel_combustivel": valores.get("nivel_combustivel", "nao_informado"),
            "observacoes": valores.get("observacoes", ""),
            "avarias": valores.get("avarias", ""),
            "pertences": valores.get("pertences", ""),
        }
    return {
        "nivel_combustivel": vistoria.nivel_combustivel,
        "observacoes": vistoria.observacoes,
        "avarias": "\n".join(f"{a.regiao} | {a.descricao}" for a in vistoria.avarias),
        "pertences": "\n".join(p.descricao for p in vistoria.pertences),
    }


@bp.get("/nova/<int:veiculo_id>")
def nova(veiculo_id):
    veiculo = db.session.get(Veiculo, veiculo_id)
    if veiculo is None or not veiculo.ativo:
        abort(404)
    return render_template("vistorias/nova.html", veiculo=veiculo)


@bp.post("/iniciar/<int:veiculo_id>")
def iniciar(veiculo_id):
    veiculo = db.session.get(Veiculo, veiculo_id)
    if veiculo is None or not veiculo.ativo:
        abort(404)

    agendamento_id = request.form.get("agendamento_id", "").strip()
    if agendamento_id:
        if not agendamento_id.isdecimal():
            return "Agendamento inválido.", 422
        # Evita atribuir a um veículo o agendamento pertencente a outro.
        from app.agendamentos.models import Agendamento

        agenda = db.session.get(Agendamento, int(agendamento_id))
        if agenda is None or agenda.veiculo_id != veiculo_id:
            return "Agendamento não pertence a este veículo.", 422
        if db.session.query(Vistoria).filter_by(agendamento_id=agenda.id).first():
            return "Agendamento já possui vistoria.", 422
        agendamento_id = agenda.id
    else:
        agendamento_id = None

    vistoria = Vistoria(
        veiculo_id=veiculo_id,
        agendamento_id=agendamento_id,
        iniciada_em=agora_utc_iso(),
        status="EmPreenchimento",
        nivel_combustivel="nao_informado",
        observacoes="",
    )
    db.session.add(vistoria)
    db.session.commit()
    return redirect(url_for("vistorias.detalhe", vistoria_id=vistoria.id), code=303)


@bp.route("/<int:vistoria_id>", methods=["GET", "POST"])
def detalhe(vistoria_id):
    vistoria = _obter_vistoria(vistoria_id)
    erro = None
    campos = _campos(vistoria)

    if request.method == "POST":
        if vistoria.status != "EmPreenchimento":
            erro = "Uma vistoria finalizada não pode ser alterada."
        else:
            campos = _campos(vistoria, request.form)
            try:
                if campos["nivel_combustivel"] not in COMBUSTIVEIS:
                    raise ValueError("Selecione um nível de combustível válido.")
                if len(campos["observacoes"]) > 3000:
                    raise ValueError("Observações devem ter até 3000 caracteres.")
                avarias = interpretar_avarias(campos["avarias"])
                pertences = interpretar_pertences(campos["pertences"])
            except ValueError as exc:
                erro = str(exc)
            else:
                vistoria.nivel_combustivel = campos["nivel_combustivel"]
                vistoria.observacoes = campos["observacoes"].strip()
                for item in list(vistoria.avarias):
                    db.session.delete(item)
                for item in list(vistoria.pertences):
                    db.session.delete(item)
                db.session.flush()
                for regiao, descricao in avarias:
                    db.session.add(Avaria(vistoria_id=vistoria.id, regiao=regiao, descricao=descricao))
                for descricao in pertences:
                    db.session.add(Pertence(vistoria_id=vistoria.id, descricao=descricao))
                db.session.commit()
                return redirect(url_for("vistorias.detalhe", vistoria_id=vistoria.id), code=303)

    return render_template(
        "vistorias/detalhe.html", vistoria=vistoria, campos=campos, erro=erro,
        combustiveis=COMBUSTIVEIS,
    ), (422 if erro else 200)
