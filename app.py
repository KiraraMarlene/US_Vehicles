import pandas as pd
import plotly.express as px
import streamlit as st

# La ruta ahora es relativa, asumiendo que el archivo está en el mismo directorio que app.py
file_path = 'vehicles_us.csv'

# Leer los datos del archivo CSV en un DataFrame
car_data = pd.read_csv(file_path)

# Título de la aplicación
st.header('Análisis de datos de ventas de coches')

# --- Opción 1: Usando botones ---
# Crea un botón para el histograma
hist_button = st.button('Construir histograma')

# Si se hace clic en el botón, crea y muestra el histograma
if hist_button:
    # Escribe un mensaje en la aplicación
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')

    # Crea un histograma con Plotly Express
    fig = px.histogram(car_data, x='odometer', title='Distribución del Odómetro')

    # Muestra el gráfico Plotly interactivo en la aplicación
    st.plotly_chart(fig, use_container_width=True)

# Crea un botón para el gráfico de dispersión
scatter_button = st.button('Construir gráfico de dispersión')

# Si se hace clic en el botón, crea y muestra el gráfico de dispersión
if scatter_button:
    # Escribe un mensaje en la aplicación
    st.write('Creación de un gráfico de dispersión para el conjunto de datos de anuncios de venta de coches')

    # Crea un gráfico de dispersión con Plotly Express
    fig = px.scatter(car_data, x='odometer', y='price', title='Relación entre Odómetro y Precio')

    # Muestra el gráfico Plotly interactivo en la aplicación
    st.plotly_chart(fig, use_container_width=True)

# --- Opción 2: Desafío con casillas de verificación ---
st.write("---") # Separador para mejor visualización
st.subheader("Opcional: Gráficos con casillas de verificación")

# Crea las casillas de verificación
build_histogram_checkbox = st.checkbox('Construir un histograma para el odómetro')
build_scatter_checkbox = st.checkbox('Construir un gráfico de dispersión para odómetro y precio')

# Si la casilla del histograma está seleccionada, lo crea
if build_histogram_checkbox:
    st.write('Construyendo un histograma para la columna de odómetro')
    fig_hist = px.histogram(car_data, x='odometer', title='Distribución del Odómetro')
    st.plotly_chart(fig_hist, use_container_width=True)

# Si la casilla del gráfico de dispersión está seleccionada, lo crea
if build_scatter_checkbox:
    st.write('Construyendo un gráfico de dispersión para la relación entre odómetro y precio')
    fig_scatter = px.scatter(car_data, x='odometer', y='price', title='Relación entre Odómetro y Precio')
    st.plotly_chart(fig_scatter, use_container_width=True)