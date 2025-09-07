import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from db_connection import load_table

dash.register_page(__name__, path="/rfm", name="RFM Segmentation")

def layout():
    df = load_table("probabilidad_compra")

    # Asegurar valores válidos
    df["cart"] = df["cart"].fillna(0)
    df["purchase"] = df["purchase"].fillna(0)
    df["total_gasto"] = df["total_gasto"].fillna(0)

    # Quartiles (manejo de duplicados con `duplicates="drop"`)
    df["F"] = pd.qcut(df["cart"], 4, labels=False, duplicates="drop")
    df["M"] = pd.qcut(df["total_gasto"], 4, labels=False, duplicates="drop")
    df["R"] = pd.qcut(df["purchase"], 4, labels=False, duplicates="drop")

    # Segmento RFM
    df["RFM_Segment"] = df["R"].astype(str) + df["F"].astype(str) + df["M"].astype(str)

    # ✅ Conteo seguro de segmentos
    seg_counts = (
        df.groupby("RFM_Segment")
        .size()
        .reset_index(name="count")   # columna única "count"
    )

    # Gráfico de barras
    fig = px.bar(
        seg_counts,
        x="RFM_Segment",
        y="count",
        labels={"RFM_Segment": "Segmento RFM", "count": "Número de Usuarios"},
        title="Distribución de Segmentos RFM",
        text_auto=True
    )
    fig.update_layout(template="plotly_white", height=500, xaxis=dict(tickangle=45))

    # Gráfico adicional pie chart (opcional)
    pie_fig = px.pie(
        seg_counts,
        names="RFM_Segment",
        values="count",
        title="Participación de Segmentos RFM"
    )
    pie_fig.update_traces(textposition="inside", textinfo="percent+label")

    return dbc.Container(
        [
            html.H2("Análisis RFM", className="mb-4"),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=fig)], md=6, xs=12),
                dbc.Col([dcc.Graph(figure=pie_fig)], md=6, xs=12),
            ])
        ],
        fluid=True,
    )
