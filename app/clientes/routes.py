from flask import current_app, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.clientes import bp
from app.clientes.models import Cliente, Veiculo
from app.clientes.servicos import normalizar_placa, validar_cliente, validar_veiculo
from app.extensions import db


def _placa_existente(placa):
    return db.session.query(Veiculo.id).filter_by(placa=placa).first() is not None


@bp.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    valores = {"nome": "", "telefone": "", "placa": "", "modelo": "", "ano": ""}
    erro = None

    if request.method == "POST":
        valores = {chave: request.form.get(chave, "") for chave in valores}
        try:
            nome, telefone = validar_cliente(valores["nome"], valores["telefone"])
            placa, modelo, ano = validar_veiculo(
                valores["placa"], valores["modelo"], valores["ano"]
            )
            if _placa_existente(placa):
                raise ValueError("Placa já cadastrada. Localize o veículo existente.")
        except ValueError as exc:
            erro = str(exc)
        else:
            cliente = Cliente(nome=nome, telefone=telefone, ativo=True)
            db.session.add(cliente)
            db.session.flush()
            db.session.add(
                Veiculo(
                    cliente_id=cliente.id, placa=placa, modelo=modelo,
                    ano=ano, ativo=True,
                )
            )
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                erro = "Placa já cadastrada. Localize o veículo existente."
            else:
                return redirect(url_for("clientes.lista_veiculos"), code=303)

    return render_template(
        "clientes/novo.html", valores=valores, erro=erro
    ), (422 if erro else 200)


@bp.route("/veiculos/novo", methods=["GET", "POST"])
def novo_veiculo():
    clientes = db.session.query(Cliente).filter_by(ativo=True).order_by(Cliente.nome).all()
    valores = {"cliente_id": "", "placa": "", "modelo": "", "ano": ""}
    erro = None

    if request.method == "POST":
        valores = {chave: request.form.get(chave, "") for chave in valores}
        if not valores["cliente_id"].isdecimal():
            erro = "Selecione um cliente válido."
        else:
            cliente = db.session.get(Cliente, int(valores["cliente_id"]))
            if cliente is None or not cliente.ativo:
                erro = "Cliente inexistente ou inativo."

        if erro is None:
            try:
                placa, modelo, ano = validar_veiculo(
                    valores["placa"], valores["modelo"], valores["ano"]
                )
                if _placa_existente(placa):
                    raise ValueError("Placa já cadastrada. Localize o veículo existente.")
            except ValueError as exc:
                erro = str(exc)
            else:
                db.session.add(
                    Veiculo(
                        cliente_id=cliente.id, placa=placa, modelo=modelo,
                        ano=ano, ativo=True,
                    )
                )
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    erro = "Placa já cadastrada. Localize o veículo existente."
                else:
                    return redirect(url_for("clientes.lista_veiculos"), code=303)

    return render_template(
        "clientes/veiculo_novo.html", clientes=clientes, valores=valores, erro=erro
    ), (422 if erro else 200)


@bp.get("/veiculos")
def lista_veiculos():
    busca = request.args.get("placa", "").strip()
    erro = None
    consulta = db.session.query(Veiculo).order_by(Veiculo.placa)
    if busca:
        try:
            placa = normalizar_placa(busca)
        except ValueError as exc:
            erro = str(exc)
            veiculos = []
        else:
            veiculos = consulta.filter(Veiculo.placa.contains(placa)).all()
    else:
        veiculos = consulta.all()

    return render_template(
        "clientes/veiculos.html",
        veiculos=veiculos,
        busca=busca,
        erro=erro,
        historico_disponivel="clientes.historico" in current_app.view_functions,
        vistoria_disponivel="vistorias.nova" in current_app.view_functions,
    )
