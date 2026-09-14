# Análisis financiero de petroleras SHELL, YPF Y EXXON MOBIL

import yfinance as yf
import plotly.express as px
import pandas as pd

data = yf.download(["SHEL", "YPF", "XOM"], period="1y")

cierre = data["Close"]

valor_maximo = round(cierre.max(), 2)
vslor_medio = round(cierre.mean(), 2)
valor_minimo = round(cierre.min(), 2)

print(valor_maximo)

fig = px.line(cierre,
        title="Cotización histórica (12 meses)",
        labels={"Date": "Fecha", "value": "Precio", "variable": "Ticker"},
        template="plotly_dark")

fig.show()