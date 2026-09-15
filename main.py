# Análisis financiero de petroleras SHELL, YPF Y EXXON MOBIL

import yfinance as yf
import plotly.express as px
import pandas as pd
import os

from google import genai as gem
from dotenv import load_dotenv

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

#fig.show()

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

print(informe_ia.text)