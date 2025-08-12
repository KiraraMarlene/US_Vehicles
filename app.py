import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# La ruta ahora es relativa, asumiendo que el archivo está en el mismo directorio que app.py
file_path = 'vehicles_us.csv'

# Leer los datos del archivo CSV en un DataFrame
car_data = pd.read_csv(file_path)

# ----------------- Sección 1: Cabecera y Data Viewer -----------------
st.header('Análisis de datos de ventas de coches')
st.write("Explora los datos de anuncios de coches usando este panel interactivo.")

# Identificar fabricantes con menos de 1000 anuncios
manufacturer_counts = car_data['manufacturer'].value_counts()
manufacturers_to_remove = manufacturer_counts[manufacturer_counts < 1000].index.tolist()

# Crear un checkbox para incluir/excluir fabricantes pequeños
show_small_manufacturers = st.checkbox('Incluir fabricantes con menos de 1000 anuncios')

# Filtrar los datos basados en la selección del checkbox
if not show_small_manufacturers:
    filtered_data = car_data[~car_data['manufacturer'].isin(manufacturers_to_remove)]
else:
    filtered_data = car_data.copy()

# Mostrar el visor de datos
st.write("### Vista de los datos")
st.dataframe(filtered_data, use_container_width=True)

# ----------------- Sección 2: Tipos de Vehículo por Fabricante -----------------
st.write("---")
st.write("### Tipos de Vehículo por Fabricante")

# Obtener la lista de fabricantes para el selectbox
manufacturers = filtered_data['manufacturer'].unique()
selected_manufacturer = st.selectbox('Selecciona un fabricante', manufacturers)

# Filtrar datos por el fabricante seleccionado
manufacturer_data = filtered_data[filtered_data['manufacturer'] == selected_manufacturer]

# Crear un gráfico de barras de los tipos de vehículos
st.write(f'Tipos de vehículos para {selected_manufacturer}')
fig_bar = px.bar(manufacturer_data['type'].value_counts().reset_index(),
                 x='index', y='type',
                 labels={'index': 'Tipo de Vehículo', 'type': 'Cantidad de Anuncios'},
                 title=f'Tipos de Vehículo de {selected_manufacturer}')
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- Sección 3: Condición vs. Año del Modelo -----------------
st.write("---")
st.write("### Condición vs. Año del Modelo")

# Obtener la lista de condiciones para el selectbox
conditions = sorted(filtered_data['condition'].unique())
selected_condition = st.selectbox('Selecciona una condición', conditions)

# Filtrar los datos por la condición seleccionada
condition_data = filtered_data[filtered_data['condition'] == selected_condition]

# Crear un histograma de los años del modelo
st.write(f'Distribución de años de modelo para vehículos en condición "{selected_condition}"')
fig_hist_condition = px.histogram(condition_data, x='model_year',
                                  title=f'Distribución de Años de Modelo ({selected_condition})',
                                  labels={'model_year': 'Año del Modelo'})
st.plotly_chart(fig_hist_condition, use_container_width=True)

# ----------------- Sección 4: Comparación de Precios entre Fabricantes -----------------
st.write("---")
st.write("### Comparación de precios entre fabricantes")

# Crear selectboxes para seleccionar dos fabricantes
manuf_options = filtered_data['manufacturer'].unique().tolist()
selected_manuf_1 = st.selectbox('Selecciona el fabricante 1', manuf_options, index=0)
selected_manuf_2 = st.selectbox('Selecciona el fabricante 2', manuf_options, index=1)

# Checkbox para normalizar el histograma
normalize_checkbox = st.checkbox('Normalizar histogramas para comparar distribuciones')

# Filtrar datos para los dos fabricantes seleccionados
manuf_1_data = filtered_data[filtered_data['manufacturer'] == selected_manuf_1]['price']
manuf_2_data = filtered_data[filtered_data['manufacturer'] == selected_manuf_2]['price']

# Crear la figura para el histograma
fig_compare = go.Figure()

# Añadir el primer histograma
fig_compare.add_trace(go.Histogram(x=manuf_1_data, name=selected_manuf_1,
                                 histnorm='probability density' if normalize_checkbox else '',
                                 marker_color='indianred'))

# Añadir el segundo histograma
fig_compare.add_trace(go.Histogram(x=manuf_2_data, name=selected_manuf_2,
                                 histnorm='probability density' if normalize_checkbox else '',
                                 marker_color='lightseagreen'))

# Actualizar el layout del gráfico
fig_compare.update_layout(barmode='overlay',
                          title_text=f'Comparación de Precios entre {selected_manuf_1} y {selected_manuf_2}',
                          xaxis_title_text='Precio (USD)',
                          yaxis_title_text='Frecuencia' if not normalize_checkbox else 'Densidad de Probabilidad',
                          bargap=0.1)

# Reducir la opacidad para que se puedan ver ambos histogramas
fig_compare.update_traces(opacity=0.75)

# Mostrar el gráfico comparativo
st.plotly_chart(fig_compare, use_container_width=True)