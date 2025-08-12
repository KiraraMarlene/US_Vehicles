import pandas as pd
import streamlit as st

# La ruta es relativa, asumiendo que el archivo está en el mismo directorio que app.py
file_path = 'vehicles_us.csv'

# Leer los datos del archivo CSV en un DataFrame
car_data = pd.read_csv(file_path)

# ----------------- Sección 1: Cabecera y Data Viewer -----------------
st.header('Análisis de datos de ventas de coches')
st.write("Explora los datos del archivo CSV a continuación:")

# Mostrar el visor de datos
st.dataframe(car_data, use_container_width=True)