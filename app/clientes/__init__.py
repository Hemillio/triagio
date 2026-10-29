from flask import Blueprint

bp = Blueprint("clientes", __name__, template_folder="templates")

from app.clientes import routes  # noqa: E402,F401
