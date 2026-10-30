from secrets import token_urlsafe

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.portal.models import TokenAcesso
from app.vistorias.servicos import agora_utc_iso


def consultar_token(texto):
    if not texto or len(texto) > 128:
        return None
    return db.session.query(TokenAcesso).filter_by(token=texto).first()


def obter_ou_criar_token(vistoria):
    existente = db.session.query(TokenAcesso).filter_by(vistoria_id=vistoria.id).first()
    if existente is not None:
        return existente

    for _ in range(3):
        registro = TokenAcesso(
            vistoria_id=vistoria.id,
            token=token_urlsafe(32),
            criado_em=agora_utc_iso(),
        )
        db.session.add(registro)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Uma requisição concorrente pode ter criado o token.
            existente = db.session.query(TokenAcesso).filter_by(vistoria_id=vistoria.id).first()
            if existente is not None:
                return existente
        else:
            return registro

    raise RuntimeError("Não foi possível reservar um token de acesso único.")
