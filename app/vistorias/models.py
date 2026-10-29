
from app.extensions import db


class Vistoria(db.Model):
    __tablename__ = "vistorias"

    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id"), nullable=False, index=True)
    agendamento_id = db.Column(
        db.Integer, db.ForeignKey("agendamentos.id"), nullable=True, unique=True
    )
    iniciada_em = db.Column(db.String(40), nullable=False)
    finalizada_em = db.Column(db.String(40), nullable=True)
    status = db.Column(db.String(24), nullable=False, default="EmPreenchimento")
    nivel_combustivel = db.Column(db.String(20), nullable=False, default="nao_informado")
    observacoes = db.Column(db.Text, nullable=False, default="")

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('EmPreenchimento', 'Finalizada', 'LaudoDisponivel')",
            name="ck_vistorias_status",
        ),
    )

    veiculo = db.relationship("Veiculo")
    avarias = db.relationship("Avaria", back_populates="vistoria", lazy="selectin")
    pertences = db.relationship("Pertence", back_populates="vistoria", lazy="selectin")
    fotos = db.relationship("Foto", back_populates="vistoria", lazy="selectin")


class Avaria(db.Model):
    __tablename__ = "avarias"

    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(db.Integer, db.ForeignKey("vistorias.id"), nullable=False)
    regiao = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)

    vistoria = db.relationship("Vistoria", back_populates="avarias")


class Pertence(db.Model):
    __tablename__ = "pertences"

    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(db.Integer, db.ForeignKey("vistorias.id"), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)

    vistoria = db.relationship("Vistoria", back_populates="pertences")


class Foto(db.Model):
    __tablename__ = "fotos"

    id = db.Column(db.Integer, primary_key=True)
    vistoria_id = db.Column(db.Integer, db.ForeignKey("vistorias.id"), nullable=False)
    caminho_arquivo = db.Column(db.String(300), nullable=False, unique=True)
    tamanho_bytes = db.Column(db.Integer, nullable=False)

    vistoria = db.relationship("Vistoria", back_populates="fotos")
