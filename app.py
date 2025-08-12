import pandas as pd
import streamlit as st

# La ruta es relativa, asumiendo que el archivo está en el mismo directorio que app.py
file_path = 'vehicles_us.csv'

# Leer los datos del archivo CSV en un DataFrame
car_data = pd.read_csv(file_path)

# Título del tablero
st.title('Data Viewer')

# ----------------- Sección 1: Cabecera y Data Viewer -----------------
st.header('Análisis de datos de ventas de coches')
st.write("Explora los datos del archivo CSV a continuación:")

# Crea un checkbox para incluir/excluir anuncios con más de 1000 millas
exclude_high_mileage = st.checkbox('Excluir anuncios con más de 1000 millas')

# Crea un botón para mostrar los datos
show_data_button = st.button('Mostrar Datos')

# Lógica para mostrar los datos
if show_data_button:
    if exclude_high_mileage:
        # Filtrar los datos para excluir los anuncios con más de 1000 millas
        filtered_data = car_data[car_data['odometer'] <= 1000]
        st.dataframe(filtered_data, use_container_width=True)
        st.write('Mostrando datos con odómetro menor o igual a 1000 millas.')
    else:
        # Mostrar todos los datos si el checkbox no está marcado
        st.dataframe(car_data, use_container_width=True)
        st.write('Mostrando todos los datos.')