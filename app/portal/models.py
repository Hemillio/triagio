from app.extensions import db


class TokenAcesso(db.Model):
    __tablename__ = "tokens_acesso"

    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(
        db.Integer,
        db.ForeignKey("vistorias.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    token = db.Column(db.String(128), nullable=False, unique=True, index=True)
    criado_em = db.Column(db.String(40), nullable=False)

    vistoria = db.relationship("Vistoria")


class Laudo(db.Model):
    __tablename__ = "laudos"

    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(
        db.Integer,
        db.ForeignKey("vistorias.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    emitido_em = db.Column(db.String(40), nullable=False)
    caminho_arquivo = db.Column(db.String(300), nullable=False, unique=True)

    vistoria = db.relationship("Vistoria")
