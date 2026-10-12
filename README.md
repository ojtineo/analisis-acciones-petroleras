# Análisis de acciones de empresas petroleras

## Descripción del proyecto

Aplicación desarrollada en Python para consultar y analizar las cotizaciones históricas de acciones de empresas del sector petrolero.

El programa obtiene datos financieros, genera una gráfica interactiva, solicita un análisis con inteligencia artificial, crea un informe en PDF y automatiza el envío de los archivos por correo electrónico.

## Tecnologías utilizadas
## Tecnologías y bibliotecas utilizadas

- Python: lenguaje utilizado para desarrollar la aplicación y automatizar el proceso de análisis.
- yfinance: obtiene cotizaciones históricas de acciones de empresas petroleras.
- Pandas: organiza y manipula los datos financieros.
- Plotly: genera gráficas interactivas para visualizar la evolución de las cotizaciones.
- Google GenAI: permite conectar la aplicación con Gemini para generar un análisis mediante inteligencia artificial.
- python-dotenv: permite leer variables de entorno desde el archivo `.env` para mantener las credenciales fuera del código fuente.
- ReportLab: genera informes financieros en formato PDF.
- SMTP: permite automatizar el envío del informe y la gráfica por correo electrónico mediante Gmail.

## Gráfica interactiva

Consulta la gráfica histórica de las cotizaciones de YPF, Shell y ExxonMobil:

[Ver gráfica interactiva de acciones petroleras](https://ojtineo.github.io/grafica-acciones-petroleras/)

## Seguridad

Las credenciales y claves de acceso se configuran mediante variables de entorno y no deben publicarse en el repositorio.

## Objetivo

Aplicar herramientas de análisis de datos y automatización para transformar información financiera en visualizaciones e informes que puedan compartirse por correo electrónico.