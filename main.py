# Análisis financiero de petroleras SHELL, YPF Y EXXON MOBIL

import yfinance as yf
import plotly.express as px
import pandas as pd
import os
import reportlab
import re
import smtplib

from google import genai as gem
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from xml.sax.saxutils import escape
from email.message import EmailMessage
from pathlib import Path



def enviar_correo_pdf(ruta_pdf):
    archivo = Path(ruta_pdf)
    
    destinatarios = os.getenv("DESTINATARIOS", "").split(",")
    destinatarios = [correo.strip() for correo in destinatarios if correo.strip()]
    
    if not archivo.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {archivo.resolve()}")

    mensaje = EmailMessage()
    mensaje["Subject"] = "Informe de análisis financiero"
    mensaje["From"] = GMAIL_USER
    mensaje["To"] = ", ".join(destinatarios)

    mensaje.set_content(
        "Adjunto encontrarás el informe de análisis financiero "
        "generado con Python.")

    
    # Adjuntar el archivo HTML
    ruta_html = "Gráfica de acciones.html"

    with open(ruta_html, "rb") as archivo_html:
        contenido_html = archivo_html.read()

    mensaje.add_attachment(
        contenido_html,
        maintype="text",
        subtype="html",
        filename="Gráfica de acciones.html")

    mensaje.add_attachment(
        archivo.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=archivo.name)

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        servidor.send_message(mensaje)

    #print("Informe PDF enviado correctamente.")

load_dotenv()


GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

data = yf.download(["SHEL", "YPF", "XOM"], period="1y")

cierre = data["Close"]

valor_maximo = round(cierre.max(), 2)
vslor_medio = round(cierre.mean(), 2)
valor_minimo = round(cierre.min(), 2)

fig = px.line(cierre,
        title="Cotización histórica (12 meses)",
        labels={"Date": "Fecha", "value": "Precio", "variable": "Ticker"},
        template="plotly_dark")

fig.write_html("index.html",
        include_plotlyjs=True,
        full_html=True)

cliente = gem.Client(api_key=GEMINI_API_KEY)

prompt = f"""Actúa como un especialista en análisis financiero.
Analiza el comportamiento de las acciones de las empresas SHELL, YPF y EXXON MOBIL,
tomando en cuenta los eventos y noticias comprobables que justifiquen las altas y bajas.
{cierre}
"""

informe_ia = cliente.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)


"""Para crear archivo .pdf con informe_ia.text importamos la lib re (regular expression) y
para convertir negritas de Markdown que trae informe_ia"""

def markdown_a_reportlab (texto):

    texto = escape(texto) #Protección de caracteres especiales
    texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto) #Conversión de texto en negritas
    return texto

texto_formateado = markdown_a_reportlab(informe_ia.text)

#Creación de archivo inf_petr.pdf

doc = SimpleDocTemplate(
    "inf_petr.pdf",
    pagesize=A4
)

styles = getSampleStyleSheet()

estilo_viñeta = ParagraphStyle(
    "Viñeta",
    parent=styles["Normal"],
    leftIndent=15,
    firstLineIndent=0,
    spaceAfter=4
)
contenido = []

contenido.append(
    Paragraph(
        "INFORME FINANCIERO",
        styles["Title"]
    )
)

lineas = informe_ia.text.splitlines()

i = 0

while i < len(lineas):

    linea = lineas[i].strip()

    # Línea vacía
    if not linea:
        contenido.append(Spacer(1, 8))
        i += 1
        continue

    # Títulos principales: ###
    if linea.startswith("### "):
        titulo = linea[4:]
        titulo = markdown_a_reportlab(titulo)

        contenido.append(
            Paragraph(
                titulo,
                styles["Heading2"]
            )
        )

        contenido.append(Spacer(1, 6))
        i += 1
        continue

    # Subtítulos: ####
    if linea.startswith("#### "):
        subtitulo = linea[5:]
        subtitulo = markdown_a_reportlab(subtitulo)

        contenido.append(
            Paragraph(
                subtitulo,
                styles["Heading3"]
            )
        )

        contenido.append(Spacer(1, 4))
        i += 1
        continue

    # Separador ---
    if linea == "---":
        contenido.append(Spacer(1, 8))
        i += 1
        continue

    # Tabla
    if linea.startswith("|"):

        filas = []

        while i < len(lineas) and lineas[i].strip().startswith("|"):

            fila = lineas[i].strip()

            # Ignoramos la línea de separación de Markdown
            if not re.match(r'^\|[\s:|-]+\|$', fila):

                celdas = fila.strip("|").split("|")

                celdas = [
                    Paragraph(
                        markdown_a_reportlab(celda.strip()),
                        styles["Normal"]
                    )
                    for celda in celdas
                ]

                filas.append(celdas)

            i += 1

        tabla = Table(
            filas,
            colWidths=[65, 120, 120, 120],
            repeatRows=1
        )

        tabla.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )

        contenido.append(tabla)
        contenido.append(Spacer(1, 10))

        continue

    # Listas con *
    if linea.startswith("*"):

        texto_lista = linea.lstrip("*").strip()
        texto_lista = markdown_a_reportlab(texto_lista)

        contenido.append(
            Paragraph(
                "&#8226;&nbsp;&nbsp;" + texto_lista,
                estilo_viñeta
            )
        )

        i += 1
        continue

    # Texto normal
    texto = markdown_a_reportlab(linea)

    contenido.append(
        Paragraph(
            texto,
            styles["Normal"]
        )
    )

    contenido.append(Spacer(1, 6))

    i += 1


# Construimos el PDF UNA SOLA VEZ
doc.build(contenido)

enviar_correo_pdf("inf_petr.pdf")