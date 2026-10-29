from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class HorarioInvalido(ValueError):
    pass


def converter_horario_para_utc(valor, nome_fuso="America/Araguaina"):
    """Converte um campo datetime-local para ISO 8601 UTC."""
    try:
        instante_local = datetime.strptime(valor, "%Y-%m-%dT%H:%M")
        horario_com_fuso = instante_local.replace(tzinfo=ZoneInfo(nome_fuso))
        return horario_com_fuso.astimezone(timezone.utc).isoformat(timespec="minutes")
    except (TypeError, ValueError, KeyError, ZoneInfoNotFoundError) as erro:
        raise HorarioInvalido("Informe uma data e hora válidas.") from erro


def formatar_horario_local(valor, nome_fuso="America/Araguaina"):
    horario_utc = datetime.fromisoformat(valor)
    return horario_utc.astimezone(ZoneInfo(nome_fuso)).strftime("%d/%m/%Y %H:%M")
