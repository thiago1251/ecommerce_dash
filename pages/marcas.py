import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from db_connection import load_table

dash.register_page(__name__, path="/marcas", name="Marcas")

def layout():
    df = load_table("top5_reconocidas")
    df_group = load_table("brand_group_summary")

    # Top 5 marcas
    fig1 = px.bar(df, x="brand", y="total_interactions", title="Top 5 Marcas - Interacciones",
                  text_auto=True)
    fig1.update_layout(template="plotly_white", height=400)

    # Grupo Reconocidas vs Otras
    fig2 = px.pie(df_group, names="brand_type", values="total_interactions",
                  title="Participación de mercado (Reconocidas vs Otras)")
    fig2.update_traces(textposition="inside", textinfo="percent+label")

    return dbc.Container([
        html.H2("Análisis de Marcas", className="mb-4"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig1), md=6),
                 dbc.Col(dcc.Graph(figure=fig2), md=6)])
    ], fluid=True)
