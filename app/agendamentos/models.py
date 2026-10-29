from app.extensions import db


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)

    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False,
        index=True
    )

    data_hora = db.Column(
        db.String(40),
        nullable=False,
        index=True
    )

    status = db.Column(
        db.String(24),
        nullable=False,
        default="Agendado"
    )

    __table_args__ = (
        db.CheckConstraint(
            "status = 'Agendado'",
            name="ck_agendamentos_status"
        ),
    )

    veiculo = db.relationship("Veiculo")
