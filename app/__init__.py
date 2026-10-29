from importlib import import_module
from importlib.util import find_spec
from pathlib import Path

from flask import Flask, render_template

from app.extensions import db, migrate
from config import Config


MODULOS = ("clientes", "agendamentos", "vistorias", "portal")


def _registrar_modulos(app):
    """Carrega somente os módulos já presentes no código integrado."""
    for nome in MODULOS:
        nome_pacote = f"app.{nome}"
        if find_spec(nome_pacote) is None:
            continue

        # SQLAlchemy precisa conhecer todos os modelos antes do create_all.
        # O registro aqui também permite que Flask-Migrate os enxergue.
        nome_modelos = f"{nome_pacote}.models"
        if find_spec(nome_modelos) is not None:
            import_module(nome_modelos)

        pacote = import_module(nome_pacote)
        blueprint = getattr(pacote, "bp", None)
        if blueprint is not None:
            app.register_blueprint(blueprint)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)
    _registrar_modulos(app)

    @app.get("/")
    def inicio():
        return render_template("inicio.html")

    return app