import os


class Config:
    SECRET_KEY = os.getenv("TRIAGIO_SECRET_KEY", "dev-local-nao-usar-em-producao")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TRIAGIO_DATABASE_URL", "sqlite:///triagio.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRIAGIO_TIMEZONE = os.getenv("TRIAGIO_TIMEZONE", "America/Araguaina")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
