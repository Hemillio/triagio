"""adiciona tokens de acesso

Revision ID: 9d31b8a45f0c
Revises: 7c79cb676899
Create Date: 2026-10-30 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9d31b8a45f0c"
down_revision = "7c79cb676899"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tokens_acesso",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vistoria_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=128), nullable=False),
        sa.Column("criado_em", sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(["vistoria_id"], ["vistorias.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tokens_acesso_vistoria_id", "tokens_acesso", ["vistoria_id"], unique=True
    )
    op.create_index("ix_tokens_acesso_token", "tokens_acesso", ["token"], unique=True)


def downgrade():
    op.drop_index("ix_tokens_acesso_token", table_name="tokens_acesso")
    op.drop_index("ix_tokens_acesso_vistoria_id", table_name="tokens_acesso")
    op.drop_table("tokens_acesso")
