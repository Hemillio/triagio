
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

FUSO_PALMAS = ZoneInfo("America/Araguaina")


def data_br(valor):
    """Formata datas UTC para o horário de Palmas."""

    if valor is None or valor == "":
        return "Não informado"

    try:
        if isinstance(valor, datetime):
            data = valor
        else:
            texto = str(valor).strip()
            texto = texto.replace("Z", "+00:00")
            data = datetime.fromisoformat(texto)

        # Datas sem fuso são tratadas como UTC.
        if data.tzinfo is None:
            data = data.replace(tzinfo=timezone.utc)

        data_local = data.astimezone(FUSO_PALMAS)

        return data_local.strftime("%d/%m/%Y às %H:%M")

    except (ValueError, TypeError, OverflowError):
        return str(valor)
