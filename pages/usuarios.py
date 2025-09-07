import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from db_connection import load_table

dash.register_page(__name__, path="/usuarios", name="Usuarios")

def layout():
    df = load_table("perfil_clientes")

    fig = px.pie(df, names="num_usuarios", values="count",
                 title="Distribución de Perfiles de Clientes")
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(template="plotly_white", height=500)

    bar = px.bar(df, x="num_usuarios", y="count", text_auto=True,
                 title="Usuarios por Perfil")
    bar.update_layout(template="plotly_white", height=400)

    return dbc.Container([
        html.H2("Perfiles de Usuarios", className="mb-4"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig), md=6),
                 dbc.Col(dcc.Graph(figure=bar), md=6)]),
    ], fluid=True)
