
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from flask import abort, current_app, redirect, request, send_from_directory, url_for
from PIL import Image, UnidentifiedImageError

from app.extensions import db
from app.vistorias import bp
from app.vistorias.models import Foto, Vistoria

MAX_FOTOS = 4
MAX_BYTES = 3 * 1024 * 1024
FORMATOS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}


def _pasta_raiz():
    return Path(current_app.instance_path) / "uploads" / "vistorias"


@bp.post("/<int:vistoria_id>/fotos")
def anexar_foto(vistoria_id):
    vistoria = db.session.get(Vistoria, vistoria_id)
    if vistoria is None:
        abort(404)
    if vistoria.status != "EmPreenchimento":
        return "Não é permitido adicionar fotos depois de finalizar a vistoria.", 422
    if db.session.query(Foto).filter_by(vistoria_id=vistoria_id).count() >= MAX_FOTOS:
        return "Limite de 4 fotos por vistoria atingido.", 422

    arquivo = request.files.get("foto")
    if arquivo is None or not arquivo.filename:
        return "Escolha uma foto para enviar.", 422

    conteudo = arquivo.stream.read(MAX_BYTES + 1)
    if len(conteudo) > MAX_BYTES:
        return "A foto deve ter no máximo 3 MB.", 422
    if not conteudo:
        return "A foto está vazia.", 422

    try:
        with Image.open(BytesIO(conteudo)) as imagem:
            formato = imagem.format
            imagem.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        return "O arquivo enviado não é uma imagem válida.", 422

    if formato not in FORMATOS:
        return "Formato inválido. Use JPEG, PNG ou WEBP.", 422

    nome = uuid4().hex + FORMATOS[formato]
    relativa = Path(str(vistoria_id)) / nome
    destino = _pasta_raiz() / relativa
    destino.parent.mkdir(parents=True, exist_ok=True)

    try:
        destino.write_bytes(conteudo)
        foto = Foto(
            vistoria_id=vistoria_id,
            caminho_arquivo=relativa.as_posix(),
            tamanho_bytes=len(conteudo),
        )
        db.session.add(foto)
        db.session.commit()
    except Exception:
        db.session.rollback()
        destino.unlink(missing_ok=True)
        raise

    return redirect(url_for("vistorias.detalhe", vistoria_id=vistoria.id), code=303)


@bp.get("/<int:vistoria_id>/fotos/<int:foto_id>")
def exibir_foto(vistoria_id, foto_id):
    foto = db.session.get(Foto, foto_id)
    if foto is None or foto.vistoria_id != vistoria_id:
        abort(404)
    return send_from_directory(_pasta_raiz(), foto.caminho_arquivo)
