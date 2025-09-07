import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from db_connection import load_table

dash.register_page(__name__, path="/patrones", name="Patrones")

def layout():
    df = load_table("patrones_temporales")

    # Heatmap hora vs tipo
    heatmap = px.density_heatmap(df, x="tiempo", y="tipo", z="total_interactions",
                                 title="Heatmap de Interacciones por Tiempo y Tipo de Evento",
                                 labels={"tiempo":"Tiempo","tipo":"Tipo Evento"})
    heatmap.update_layout(template="plotly_white", height=500)

    # Tendencia
    line = px.line(df, x="tiempo", y="total_interactions", color="tipo",
                   title="Tendencia de Eventos en el Tiempo")
    line.update_layout(template="plotly_white", height=400)

    return dbc.Container([
        html.H2("Patrones Temporales", className="mb-4"),
        dbc.Row([dbc.Col(dcc.Graph(figure=heatmap), md=12)]),
        dbc.Row([dbc.Col(dcc.Graph(figure=line), md=12)]),
    ], fluid=True)
