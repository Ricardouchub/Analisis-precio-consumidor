# --- Importar Librerías ---
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# --- Carga y Preparación de Datos ---
DATA_PATH = 'data/precios_limpio.parquet'
try:
    df = pd.read_parquet(DATA_PATH)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta '{DATA_PATH}'.")
    print("Asegúrate de que el archivo CSV limpio esté en la carpeta 'data'.")
    exit()

df['anio_mes'] = df['anio'].astype(str) + '-' + df['mes'].astype(str).str.zfill(2)

# Listas para opciones de filtros
ALL_REGIONS = sorted(df['region'].unique())
ALL_CANALES = sorted(df['tipo_de_punto_monitoreo'].unique())

# --- Inicialización de la App Dash ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])
server = app.server

# --- Estilos ---
SIDEBAR_STYLE = {"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "22rem", "padding": "2rem 1rem", "background-color": "#f8f9fa", "overflow-y": "auto"}
CONTENT_STYLE = {"margin-left": "24rem", "margin-right": "2rem", "padding": "2rem 1rem"}

# --- Layout de la App ---
app.layout = html.Div([
    html.Div([
        html.P("Filtra los datos para explorar:", className="lead"),
        dbc.Label("Rango de Años:"),
        dcc.RangeSlider(id='filtro-anio', min=df['anio'].min(), max=df['anio'].max(), step=1, value=[df['anio'].min(), df['anio'].max()], marks={str(year): str(year) for year in df['anio'].unique()}, tooltip={"placement": "bottom", "always_visible": True}),
        html.Div([dbc.Label("Región(es):", className="mt-4"), dbc.Button("Seleccionar/Quitar Todas", id="boton-seleccionar-todas-regiones", color="secondary", size="sm", className="ms-2")], className="d-flex align-items-center"),
        dcc.Dropdown(id='filtro-region', options=[{'label': i, 'value': i} for i in ALL_REGIONS], value=ALL_REGIONS, multi=True),
        dbc.Label("Punto de Monitoreo:", className="mt-4"),
        dcc.Dropdown(id='filtro-canal', options=[{'label': i, 'value': i} for i in ALL_CANALES], value=ALL_CANALES, multi=True),
        dbc.Label("Grupo de Alimento:", className="mt-4"),
        dcc.Dropdown(id='filtro-grupo', options=[{'label': i, 'value': i} for i in sorted(df['grupo'].unique())], value='Carne bovina', clearable=False),
        dbc.Label("Producto(s):", className="mt-4"),
        dcc.Dropdown(id='filtro-producto', multi=True),
    ], style=SIDEBAR_STYLE),
    
    html.Div(id="page-content", style=CONTENT_STYLE, children=[
        html.Div([
            html.H4("Visualizador de precios al consumidor (Chile 2020-2025)", className="fw-bold"),
            dcc.Markdown(
                """
                Este dashboard interactivo presenta un análisis de más de 1.8 millones de registros de precios al consumidor, capturados por la **Oficina de Estudios y Políticas Agrarias (ODEPA)** entre 2020 y 2025. 
                La plataforma permite explorar la evolución de precios de los principales alimentos en distintas regiones y canales de venta de Chile.
                
                **¿Cómo usar?**
                * **Explore:** Utilice los filtros en el panel izquierdo.
                * **Periodo:** Seleccione un rango de años con la barra deslizante.
                * **Compare:** Escoja múltiples regiones, canales y productos. Los gráficos se actualizarán automáticamente.
                """
            )
        ]),
        
        dbc.Row([dbc.Col(dcc.Graph(id='grafico-evolucion-precio'), width=12, className="mt-4")]),
        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='grafico-comparativa-regional'), width=6),
            dbc.Col(dcc.Graph(id='grafico-distribucion-canal'), width=6) # ID cambiado para el nuevo gráfico
        ]),
        
        html.Div(
            html.Footer(
                dbc.Row([
                    dbc.Col(html.P("Realizado por: Ricardo Urdaneta", className="text-muted")),
                    dbc.Col(html.Div([
                        dbc.Button(html.I(className="bi bi-github me-2"), href="https://github.com/Ricardouchub", target="_blank", color="dark", outline=True, className="me-1 border-0"),
                        dbc.Button(html.I(className="bi bi-linkedin me-2"), href="https://www.linkedin.com/in/ricardourdanetacastro/", target="_blank", color="primary", outline=True, className="border-0")
                    ]), width="auto")
                ]),
            ),
            className="d-flex justify-content-end mt-5"
        )
    ])
])

# --- Callbacks ---
@app.callback(
    Output('filtro-producto', 'options'),
    Output('filtro-producto', 'value'),
    Input('filtro-grupo', 'value')
)
def actualizar_opciones_producto(grupo_seleccionado):
    productos = sorted(df[df['grupo'] == grupo_seleccionado]['producto'].unique())
    valores_iniciales = [productos[0]] if productos else []
    return [{'label': i, 'value': i} for i in productos], valores_iniciales

@app.callback(
    Output('filtro-region', 'value'),
    Input('boton-seleccionar-todas-regiones', 'n_clicks'),
    State('filtro-region', 'value'),
    prevent_initial_call=True
)
def seleccionar_todas_regiones(n_clicks, valores_actuales):
    if len(valores_actuales) == len(ALL_REGIONS):
        return []
    else:
        return ALL_REGIONS

@app.callback(
    Output('grafico-evolucion-precio', 'figure'),
    Output('grafico-comparativa-regional', 'figure'),
    Output('grafico-distribucion-canal', 'figure'), # Output actualizado
    Input('filtro-anio', 'value'),
    Input('filtro-region', 'value'),
    Input('filtro-canal', 'value'),
    Input('filtro-producto', 'value')
)
def actualizar_dashboard(anios, regiones, canales, productos):
    if not regiones or not productos or not canales:
        empty_fig = {"layout": {"annotations": [{"text": "Por favor, selecciona al menos una opción en cada filtro.", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}}]}}
        return empty_fig, empty_fig, empty_fig

    dff = df[
        (df['anio'].between(anios[0], anios[1])) &
        (df['region'].isin(regiones)) &
        (df['tipo_de_punto_monitoreo'].isin(canales)) &
        (df['producto'].isin(productos))
    ]

    if dff.empty:
        empty_fig = {"layout": {"annotations": [{"text": "No hay datos para esta selección.", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}}]}}
        return empty_fig, empty_fig, empty_fig

    # --- Lógica de Gráficos ---
    
    # Gráfico de Líneas
    df_temporal = dff.groupby(['anio_mes', 'producto'])['precio_promedio'].mean().reset_index().sort_values('anio_mes')
    fig_linea = px.line(df_temporal, x='anio_mes', y='precio_promedio', color='producto', title='Evolución de Precios de la Selección', markers=True)
    fig_linea.update_layout(transition_duration=500, plot_bgcolor="white", legend_title_text='Producto', height=450)

    # Gráfico de Barras Regional
    promedio_nacional_seleccion = dff['precio_promedio'].mean()
    df_regional = dff.groupby('region')['precio_promedio'].mean().reset_index()
    df_regional['diferencia_%'] = ((df_regional['precio_promedio'] - promedio_nacional_seleccion) / promedio_nacional_seleccion) * 100
    fig_regional = px.bar(df_regional.sort_values('diferencia_%', ascending=False), x='region', y='diferencia_%', title='Diferencia vs. Promedio Nacional por Región', labels={'region': '', 'diferencia_%': 'Diferencia (%)'}, height=400, color='diferencia_%', color_continuous_scale='RdBu_r')
    fig_regional.update_layout(plot_bgcolor="white", xaxis_tickangle=-45, coloraxis_showscale=False)
    
    # --- GRÁFICO DE TORTA (PIE CHART) ---
    # Contamos la cantidad de registros por canal de venta
    df_canal_dist = dff['tipo_de_punto_monitoreo'].value_counts().reset_index()
    fig_torta = px.pie(
        df_canal_dist, 
        names='tipo_de_punto_monitoreo', 
        values='count', 
        title='Distribución de Registros por Canal',
        height=400
    )
    fig_torta.update_traces(textposition='inside', textinfo='percent+label')
    fig_torta.update_layout(showlegend=False)

    return fig_linea, fig_regional, fig_torta

# --- Ejecutar el Servidor ---
if __name__ == '__main__':
    app.run(debug=True)