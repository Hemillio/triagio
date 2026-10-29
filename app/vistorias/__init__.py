
from flask import Blueprint

bp = Blueprint("vistorias", __name__, url_prefix="/vistorias", template_folder="templates")

from app.vistorias import views  # noqa: E402,F401

from app.vistorias import finalizacao  # noqa: E402,F401