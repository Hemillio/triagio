
from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    veiculos = db.relationship(
        "Veiculo",
        back_populates="cliente",
        lazy=True,
    )


class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False,
    )
    placa = db.Column(db.String(10), nullable=False, unique=True)
    modelo = db.Column(db.String(120), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    cliente = db.relationship(
        "Cliente",
        back_populates="veiculos",
    )
