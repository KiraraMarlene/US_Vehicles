import pandas as pd
import streamlit as st

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
