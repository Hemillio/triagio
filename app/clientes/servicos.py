
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def normalizar_placa(valor):
    """Padroniza a placa para cadastro e pesquisa."""
    placa = re.sub(r"[\s-]+", "", str(valor or "")).upper()

    if not placa:
        raise ValueError("Informe a placa do veículo.")

    if len(placa) > 10 or not re.fullmatch(r"[A-Z0-9]+", placa):
        raise ValueError("Informe uma placa com letras e números válidos.")

    return placa


def validar_veiculo(placa, modelo, ano):
    placa = normalizar_placa(placa)
    modelo = (modelo or "").strip()

    if not modelo or len(modelo) > 120:
        raise ValueError("Informe o modelo (até 120 caracteres).")

    try:
        numero_ano = int(str(ano).strip())
    except (TypeError, ValueError) as erro:
        raise ValueError("Informe um ano numérico válido.") from erro

    if not 1 <= numero_ano <= 9999:
        raise ValueError("Informe um ano entre 1 e 9999.")

    return placa, modelo, numero_ano


def validar_cliente(nome, telefone):
    nome = (nome or "").strip()
    telefone = (telefone or "").strip()

    if not nome or len(nome) > 120:
        raise ValueError("Informe o nome do cliente (até 120 caracteres).")

    if len(telefone) > 30:
        raise ValueError("O telefone deve ter até 30 caracteres.")

    return nome, telefone


def formatar_data_local(valor, fuso="America/Araguaina"):
    """Converte uma data ISO 8601 para o horário local."""
    if not valor:
        return "—"

    data = datetime.fromisoformat(valor)

    if data.tzinfo is None:
        data = data.replace(tzinfo=timezone.utc)

    return data.astimezone(ZoneInfo(fuso)).strftime("%d/%m/%Y %H:%M")
