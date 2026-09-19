# Análisis financiero de petroleras SHELL, YPF Y EXXON MOBIL

import yfinance as yf
import plotly.express as px
import pandas as pd
import os
import reportlab
import re

from google import genai as gem
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from xml.sax.saxutils import escape

load_dotenv()

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

fig.write_html("Gráfica de acciones.html")

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
ara convertir negritas de Markdown que trae informe_ia"""

def markdown_a_reportlab (texto):

    texto = escape(texto) #Protegemos caracteres especiales
    texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto) #Convertimos texto en negritas
    return texto

texto_formateado = markdown_a_reportlab(informe_ia.text)

doc = SimpleDocTemplate(
    "inf_petr.pdf",
    pagesize=A4
)
print(A4)