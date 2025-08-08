# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración de la Página ---
st.set_page_config(layout="wide")

# --- Carga y Preparación de Datos ---
@st.cache_data
def load_data():
    """Carga los datos desde el archivo Parquet y los prepara."""
    try:
        df = pd.read_parquet('data/precios_limpio.parquet')
        df['anio_mes'] = df['anio'].astype(str) + '-' + df['mes'].astype(str).str.zfill(2)
        return df
    except FileNotFoundError:
        st.error("Error: No se encontró el archivo 'data/precios_limpio.parquet'.")
        return None

df = load_data()

# --- Renderizado de la App ---
# Toda la lógica de la app ahora está correctamente indentada dentro de este 'if'
if df is not None:
    # --- Barra Lateral con Filtros ---
    st.sidebar.title("Instrucciones:")
    st.sidebar.markdown(
        """
        **Explore:** Utilice los filtros en este panel.
        **Periodo:** Seleccione un rango de años con la barra deslizante.
        **Compare:** Escoja múltiples regiones y/o productos. Los gráficos se actualizarán automáticamente.
        """
    )
    st.sidebar.divider()
    st.sidebar.header("Filtros del Dashboard")

    ALL_REGIONS = sorted(df['region'].unique())
    
    min_anio, max_anio = int(df['anio'].min()), int(df['anio'].max())
    selected_years = st.sidebar.slider('Rango de Años:', min_anio, max_anio, (min_anio, max_anio))

    select_all_regions = st.sidebar.checkbox("Seleccionar Todas las Regiones", value=True)
    if select_all_regions:
        selected_regions = st.sidebar.multiselect('Región(es):', ALL_REGIONS, default=ALL_REGIONS)
    else:
        selected_regions = st.sidebar.multiselect('Región(es):', ALL_REGIONS)

    selected_group = st.sidebar.selectbox('Grupo de Alimento:', sorted(df['grupo'].unique()))
    
    available_products = sorted(df[df['grupo'] == selected_group]['producto'].unique())
    selected_products = st.sidebar.multiselect('Producto(s):', available_products, default=available_products[0] if available_products else None)

    # --- Filtrar el DataFrame Principal ---
    dff = df[
        (df['anio'].between(selected_years[0], selected_years[1])) &
        (df['region'].isin(selected_regions)) &
        (df['producto'].isin(selected_products))
    ]

    # --- Contenido Principal ---
    st.header("Analisis de Precios al Consumidor del 2020 al 2025 en Chile")
    st.markdown("""
    Este dashboard interactivo presenta un análisis de precios al consumidor, capturados por la **Oficina de Estudios y Políticas Agrarias (ODEPA)** entre 2020 y 2025. 
    La plataforma permite explorar la evolución de precios de los principales alimentos en distintas regiones y canales de venta de Chile.
    """)

    if dff.empty or not selected_products:
        st.warning('No hay datos disponibles para la selección actual. Por favor, ajusta los filtros.')
    else:
        # Gráfico de Líneas
        df_temporal = dff.groupby(['anio_mes', 'producto'])['precio_promedio'].mean().reset_index().sort_values('anio_mes')
        fig_linea = px.line(df_temporal, x='anio_mes', y='precio_promedio', color='producto',
                            title='Evolución de Precios de la Selección (Promedio por Región)', markers=True)
        fig_linea.update_layout(plot_bgcolor="white", legend_title_text='Producto', height=450)
        st.plotly_chart(fig_linea, use_container_width=True)

        st.divider()

        # Gráficos Inferiores
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Barras Regional
            df_regional = dff.groupby('region')['precio_promedio'].mean().reset_index()
            fig_regional = px.bar(df_regional.sort_values('precio_promedio', ascending=False), 
                                  x='region', y='precio_promedio',
                                  title='Precio Promedio por Región',
                                  labels={'region': '', 'precio_promedio': 'Precio Promedio (CLP)'}, height=400,
                                  color='region')
            fig_regional.update_layout(plot_bgcolor="white", xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig_regional, use_container_width=True)

        with col2:
            # Gráfico de Torta
            df_canal_dist = dff['tipo_de_punto_monitoreo'].value_counts().reset_index()
            fig_torta = px.pie(df_canal_dist, names='tipo_de_punto_monitoreo', values='count',
                               title='Distribución de Registros por Canal', height=400)
            fig_torta.update_traces(textposition='inside', textinfo='percent+label')
            fig_torta.update_layout(showlegend=False)
            st.plotly_chart(fig_torta, use_container_width=True)