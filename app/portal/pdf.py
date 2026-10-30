from html import escape
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _texto(valor):
    return escape(str(valor if valor is not None else ""))


def criar_pdf_laudo(vistoria, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    estilos = getSampleStyleSheet()
    titulo = estilos["Title"]
    subtitulo = estilos["Heading2"]
    normal = estilos["BodyText"]
    elementos = [
        Paragraph("Triagio - Laudo simplificado de entrada", titulo),
        Spacer(1, 0.4 * cm),
        Paragraph(f"Vistoria n. {_texto(vistoria.id)}", normal),
        Paragraph(f"Placa: {_texto(vistoria.veiculo.placa)}", normal),
        Paragraph(f"Modelo: {_texto(vistoria.veiculo.modelo)}", normal),
        Paragraph(f"Ano: {_texto(vistoria.veiculo.ano)}", normal),
        Paragraph(f"Iniciada em (UTC): {_texto(vistoria.iniciada_em)}", normal),
        Paragraph(f"Finalizada em (UTC): {_texto(vistoria.finalizada_em)}", normal),
        Spacer(1, 0.3 * cm),
        Paragraph("Checklist de entrada", subtitulo),
        Paragraph(f"Combustível: {_texto(vistoria.nivel_combustivel)}", normal),
        Paragraph("Observações:", normal),
        Paragraph(_texto(vistoria.observacoes) or "Nenhuma.", normal),
        Spacer(1, 0.3 * cm),
        Paragraph("Avarias identificadas", subtitulo),
    ]
    if vistoria.avarias:
        for avaria in vistoria.avarias:
            elementos.append(
                Paragraph(f"- {_texto(avaria.regiao)}: {_texto(avaria.descricao)}", normal)
            )
    else:
        elementos.append(Paragraph("Nenhuma avaria registrada.", normal))

    elementos.extend([Spacer(1, 0.3 * cm), Paragraph("Pertences registrados", subtitulo)])
    if vistoria.pertences:
        for pertence in vistoria.pertences:
            elementos.append(Paragraph(f"- {_texto(pertence.descricao)}", normal))
    else:
        elementos.append(Paragraph("Nenhum pertence registrado.", normal))

    elementos.extend(
        [
            Spacer(1, 0.8 * cm),
            Paragraph("Documento gerado pelo Triagio para registro de entrada do veículo.", normal),
        ]
    )
    pdf = SimpleDocTemplate(
        str(destino),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=f"Laudo Triagio - Vistoria {vistoria.id}",
    )
    pdf.build(elementos)
