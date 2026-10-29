
from datetime import datetime, timezone

COMBUSTIVEIS = ("nao_informado", "vazio", "1/4", "1/2", "3/4", "cheio")


def agora_utc_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def interpretar_avarias(texto):
    avarias = []
    for indice, linha in enumerate(texto.splitlines(), start=1):
        linha = linha.strip()
        if not linha:
            continue
        regiao, separador, descricao = linha.partition("|")
        regiao, descricao = regiao.strip(), descricao.strip()
        if not separador or not regiao or not descricao:
            raise ValueError(f"Avaria na linha {indice}: use Região | descrição.")
        if len(regiao) > 80 or len(descricao) > 500:
            raise ValueError(f"Avaria na linha {indice}: texto acima do limite.")
        avarias.append((regiao, descricao))
    return avarias


def interpretar_pertences(texto):
    pertences = []
    for indice, linha in enumerate(texto.splitlines(), start=1):
        descricao = linha.strip()
        if not descricao:
            continue
        if len(descricao) > 250:
            raise ValueError(f"Pertence na linha {indice}: texto acima de 250 caracteres.")
        pertences.append(descricao)
    return pertences
