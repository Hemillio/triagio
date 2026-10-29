from flask import Blueprint


bp = Blueprint(
    "agendamentos",
    __name__,
    url_prefix="/agendamentos",
    template_folder="templates"
)

from app.agendamentos import routes  # noqa: E402,F401
