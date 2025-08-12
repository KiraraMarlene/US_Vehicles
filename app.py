import pandas as pd
import streamlit as st
import plotly.express as px

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