import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# La ruta es relativa, asumiendo que el archivo está en el mismo directorio que app.py
file_path = 'vehicles_us.csv'

# Leer los datos del archivo CSV en un DataFrame
car_data = pd.read_csv(file_path)

# ----------------- Modificación de datos -----------------
# Crear una nueva columna 'manufacturer' basada en la primera palabra de la columna 'model'
# Se utiliza .fillna('') para manejar valores faltantes en 'model'
car_data['manufacturer'] = car_data['model'].fillna('').apply(lambda x: str(x).split()[0] if isinstance(x, str) else '')

# ----------------- Título principal -----------------
st.title('Análisis de datos de venta de carros')

# ----------------- Sección de Data Viewer -----------------
st.header('Data Viewer')

# Lógica para contar los anuncios por fabricante
manufacturer_counts = car_data['manufacturer'].value_counts()
# Obtener una lista de fabricantes con menos de 1000 anuncios
small_manufacturers = manufacturer_counts[manufacturer_counts < 1000].index.tolist()

# Crea un checkbox para incluir/excluir fabricantes con menos de 1000 anuncios
# La lógica está invertida según la solicitud: si se hace clic, muestra todos; si no, excluye.
show_all_manufacturers = st.checkbox('Incluir fabricantes con menos de 1000 anuncios')

# Filtrar los datos basados en el estado del checkbox
if show_all_manufacturers:
    # Si la casilla está marcada, mostrar todos los datos
    filtered_data = car_data.copy()
    st.write('Mostrando todos los fabricantes.')
else:
    # Si la casilla no está marcada, excluir los fabricantes con menos de 1000 anuncios
    filtered_data = car_data[~car_data['manufacturer'].isin(small_manufacturers)]
    st.write(f'Excluyendo fabricantes con menos de 1000 anuncios. (Total de fabricantes excluidos: {len(small_manufacturers)})')

# Mostrar el visor de datos con el DataFrame filtrado
st.dataframe(filtered_data, use_container_width=True)

# ----------------- Gráfico de barras interactivo -----------------
st.header('Tipo de vehículos por productor')

# Selector interactivo para los fabricantes
manufacturers = sorted(filtered_data['manufacturer'].unique())
selected_manufacturers = st.multiselect('Selecciona el(los) productor(es)', manufacturers, default=manufacturers)

# Selector interactivo para los tipos de vehículos
vehicle_types = sorted(filtered_data['type'].unique())
selected_types = st.multiselect('Selecciona el(los) tipo(s) de vehículo', vehicle_types, default=vehicle_types)

# Filtrar los datos según el fabricante y tipo de vehículo seleccionados
data_by_selection = filtered_data[
    (filtered_data['manufacturer'].isin(selected_manufacturers)) &
    (filtered_data['type'].isin(selected_types))
]

# Agrupar los datos por fabricante y tipo y contar las ocurrencias
grouped_data = data_by_selection.groupby(['manufacturer', 'type']).size().reset_index(name='count')

# Crear el gráfico de barras con Plotly Express
fig_bar = px.bar(
    grouped_data,
    x='manufacturer',
    y='count',
    color='type',
    title='Tipos de vehículos por productor',
    labels={'manufacturer': 'Productor', 'count': 'Número de Anuncios', 'type': 'Tipo de Vehículo'}
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- Histograma de Condición vs. Año del Modelo -----------------
st.header('Condición contra año de modelo')

# Selector interactivo para la condición
conditions = sorted(filtered_data['condition'].unique())
selected_condition = st.selectbox('Selecciona una condición', conditions)

# Filtrar los datos por la condición seleccionada
condition_data = filtered_data[filtered_data['condition'] == selected_condition]

# Crear un histograma de los años del modelo
fig_hist_condition = px.histogram(condition_data, x='model_year',
                                  title=f'Distribución de años de modelo para vehículos en condición "{selected_condition}"',
                                  labels={'model_year': 'Año del Modelo'})

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_hist_condition, use_container_width=True)

# ----------------- Comparación de precios por productor -----------------
st.header('Comparar precio por productor')

# Selectores para los dos productores a comparar
manuf_options = sorted(filtered_data['manufacturer'].unique())
manuf1 = st.selectbox('Selecciona el productor 1', manuf_options, index=0)
manuf2 = st.selectbox('Selecciona el productor 2', manuf_options, index=1)

# Filtrar los datos para los productores seleccionados
data_manuf1 = filtered_data[filtered_data['manufacturer'] == manuf1]['price']
data_manuf2 = filtered_data[filtered_data['manufacturer'] == manuf2]['price']

# Crear el histograma con Plotly Graph Objects para superponer
fig_comp = go.Figure()

fig_comp.add_trace(go.Histogram(x=data_manuf1, name=manuf1, marker_color='blue'))
fig_comp.add_trace(go.Histogram(x=data_manuf2, name=manuf2, marker_color='red'))

# Actualizar el diseño del gráfico para superponer las barras
fig_comp.update_layout(barmode='overlay',
                       title_text=f'Comparación de precios entre {manuf1} y {manuf2}',
                       xaxis_title_text='Precio',
                       yaxis_title_text='Frecuencia',
                       bargap=0.1)

# Reducir la opacidad para que los histogramas superpuestos sean visibles
fig_comp.update_traces(opacity=0.75)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_comp, use_container_width=True)