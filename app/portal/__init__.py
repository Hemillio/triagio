from flask import Blueprint

bp = Blueprint("portal", __name__, template_folder="templates")

from app.portal import routes  # noqa: E402,F401
from app.portal import laudos  # noqa: E402,F401
