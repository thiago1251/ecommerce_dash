import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from db_connection import load_table

dash.register_page(__name__, path="/clv", name="CLV")

def layout():
    df = load_table("probabilidad_compra")

    # ======================
    # Supuestos
    # ======================
    margen = 0.3
    horizonte = 12  # meses

    clv_promedio = (df["gasto_promedio"].fillna(0).mean() *
                    df["compras"].fillna(0).mean() *
                    horizonte * margen)

    # ======================
    # Tarjeta de CLV
    # ======================
    clv_card = dbc.Card(
        dbc.CardBody([
            html.H4("CLV Promedio Estimado", className="card-title"),
            html.H2(f"${clv_promedio:,.0f}", className="display-4 text-success fw-bold"),
            html.P(f"Horizonte: {horizonte} meses | Margen: {margen*100:.0f}%",
                   className="text-muted"),
            dbc.Badge("Customer Lifetime Value", color="success", className="mt-2")
        ]),
        className="shadow-sm mb-4"
    )

    # ======================
    # Gráfico de distribución del gasto
    # ======================
    if "gasto_promedio" in df.columns:
        fig = px.histogram(df, x="gasto_promedio",
                           nbins=40,
                           title="Distribución del Gasto Promedio",
                           labels={"gasto_promedio": "Gasto Promedio ($)"})
        fig.update_layout(template="plotly_white", height=400)
    else:
        fig = None

    # ======================
    # Supuestos explicativos
    # ======================
    supuestos = dbc.Card(
        dbc.CardBody([
            html.H5("Supuestos utilizados", className="card-title"),
            html.Ul([
                html.Li("Margen de utilidad del 30%"),
                html.Li("Horizonte de análisis de 12 meses"),
                html.Li("Basado en gasto_promedio y número de compras"),
            ])
        ]),
        className="shadow-sm"
    )

    # ======================
    # Layout final
    # ======================
    return dbc.Container([
        html.H2("Customer Lifetime Value (CLV)", className="mb-4"),
        dbc.Row([
            dbc.Col(clv_card, xs=12, md=4),
            dbc.Col(dcc.Graph(figure=fig), xs=12, md=8) if fig else None
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(supuestos, xs=12, md=6)
        ])
    ], fluid=True)
