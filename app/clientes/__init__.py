
from flask import Blueprint

bp = Blueprint("clientes", __name__, url_prefix="/clientes")
from app.clientes import routes