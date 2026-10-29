
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.clientes import bp
from app.clientes.models import Cliente, Veiculo


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        placa = request.form.get("placa", "").strip().upper()
        placa = placa.replace("-", "").replace(" ", "")
        modelo = request.form.get("modelo", "").strip()
        ano_texto = request.form.get("ano", "").strip()

        erros = []

        if not nome or len(nome) > 120:
            erros.append("Informe o nome do cliente, com até 120 caracteres.")

        if len(telefone) > 30:
            erros.append("O telefone deve ter até 30 caracteres.")

        if not placa or len(placa) > 10 or not placa.isalnum():
            erros.append("Informe uma placa válida, com letras e números.")

        if not modelo or len(modelo) > 120:
            erros.append("Informe o modelo do veículo, com até 120 caracteres.")

        try:
            ano = int(ano_texto)
            if ano <= 0 or len(ano_texto) > 4:
                raise ValueError
        except ValueError:
            erros.append("Informe um ano válido, com até quatro dígitos.")
            ano = None

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("clientes/novo.html"), 422

        cliente = Cliente(nome=nome, telefone=telefone or None)
        veiculo = Veiculo(
            placa=placa,
            modelo=modelo,
            ano=ano,
            cliente=cliente,
        )

        try:
            db.session.add(cliente)
            db.session.add(veiculo)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Não foi possível cadastrar: essa placa já pode estar registrada.", "erro")
            return render_template("clientes/novo.html"), 422

        flash("Cliente e veículo cadastrados com sucesso!", "sucesso")
        return redirect(url_for("clientes.listar_veiculos"), code=303)

    return render_template("clientes/novo.html")
@bp.get("/veiculos")
def listar_veiculos():
    placa = request.args.get("placa", "").strip().upper()
    placa = placa.replace("-", "").replace(" ", "")

    consulta = Veiculo.query

    if placa:
        consulta = consulta.filter(Veiculo.placa.contains(placa))

    veiculos = consulta.order_by(Veiculo.placa).all()

    return render_template(
        "clientes/veiculos.html",
        veiculos=veiculos,
        placa=placa,
    )


@bp.route("/veiculos/novo", methods=["GET", "POST"])
def novo_veiculo():
    clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()

    if request.method == "POST":
        cliente_id_texto = request.form.get("cliente_id", "").strip()
        placa = request.form.get("placa", "").strip().upper()
        placa = placa.replace("-", "").replace(" ", "")
        modelo = request.form.get("modelo", "").strip()
        ano_texto = request.form.get("ano", "").strip()

        erros = []

        try:
            cliente_id = int(cliente_id_texto)
            cliente = Cliente.query.filter_by(
                id=cliente_id,
                ativo=True,
            ).first()

            if cliente is None:
                erros.append("Selecione um cliente existente e ativo.")
        except ValueError:
            cliente = None
            erros.append("Selecione um cliente válido.")

        if not placa or len(placa) > 10 or not placa.isalnum():
            erros.append("Informe uma placa válida, com letras e números.")

        if not modelo or len(modelo) > 120:
            erros.append("Informe o modelo do veículo, com até 120 caracteres.")

        try:
            ano = int(ano_texto)
            if ano <= 0 or len(ano_texto) > 4:
                raise ValueError
        except ValueError:
            erros.append("Informe um ano válido, com até quatro dígitos.")
            ano = None

        if erros:
            for erro in erros:
                flash(erro, "erro")

            return render_template(
                "clientes/veiculo_novo.html",
                clientes=clientes,
            ), 422

        veiculo = Veiculo(
            cliente_id=cliente.id,
            placa=placa,
            modelo=modelo,
            ano=ano,
        )

        try:
            db.session.add(veiculo)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(
                "Não foi possível cadastrar: essa placa já pode estar registrada.",
                "erro",
            )
            return render_template(
                "clientes/veiculo_novo.html",
                clientes=clientes,
            ), 422

        flash("Veículo cadastrado com sucesso!", "sucesso")
        return redirect(url_for("clientes.listar_veiculos"), code=303)

    return render_template(
        "clientes/veiculo_novo.html",
        clientes=clientes,
    )
