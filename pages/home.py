import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from components.kpi.kpicard import kpicard
from db_connection import load_table

dash.register_page(
    __name__,
    path="/",
    name="Inicio",
    title="Dashboard Ejecutivo - Ecommerce"
)

def layout():
    # =======================
    # Load Data
    # =======================
    df_eventos = load_table("probabilidad_compra")
    df_marcas = load_table("top5_reconocidas")
    df_patrones = load_table("patrones_temporales")
    df_categorias = load_table("conversion_categorias")

    # =======================
    # KPIs ejecutivos
    # =======================
    total_eventos = (df_eventos["cart"].sum() +
                     df_eventos["purchase"].sum() +
                     df_eventos["view"].sum())

    compras = df_eventos["purchase"].sum()
    tasa_conversion = round((compras / total_eventos) * 100, 2) if total_eventos > 0 else 0
    gmv = df_eventos["total_gasto"].sum(skipna=True) if "total_gasto" in df_eventos else compras * 100  # fallback
    aov = round(gmv / compras, 2) if compras > 0 else 0
    usuarios_activos = df_eventos["entidad"].nunique()

    kpi1 = kpicard(value=f"${gmv:,.0f}", title="GMV Total", subtitle="Ingresos estimados", icon="bi-cash-stack", color="success")
    kpi2 = kpicard(value=f"{compras:,}", title="Pedidos", subtitle="Transacciones completadas", icon="bi-bag-check", color="primary")
    kpi3 = kpicard(value=f"{tasa_conversion}%", title="Tasa Conversión", subtitle="Compras/Eventos", icon="bi-graph-up", color="info")
    kpi4 = kpicard(value=f"${aov:,.0f}", title="AOV", subtitle="Ticket promedio", icon="bi-receipt", color="warning")
    kpi5 = kpicard(value=f"{usuarios_activos:,}", title="Usuarios Activos", subtitle="Entidades únicas", icon="bi-people", color="danger")

    # =======================
    # Tendencia temporal
    # =======================
    df_patrones["rolling"] = df_patrones["total_interactions"].rolling(window=7, min_periods=1).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_patrones["tiempo"], y=df_patrones["total_interactions"],
                                   mode="lines", name="Interacciones", line=dict(color="#1f77b4", width=2)))
    fig_trend.add_trace(go.Scatter(x=df_patrones["tiempo"], y=df_patrones["rolling"],
                                   mode="lines", name="Media móvil (7d)", line=dict(color="#ff7f0e", dash="dash")))
    fig_trend.update_layout(
        title="Tendencia de actividad con media móvil",
        template="plotly_white",
        height=400,
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=30, r=30, t=60, b=30)
    )

    # =======================
    # Top categorías
    # =======================
    fig_cat = px.bar(
        df_categorias.sort_values("purchase_rate", ascending=False).head(10),
        x="category_code", y="purchase_rate",
        text_auto=".1%",
        color="purchase_rate",
        color_continuous_scale="Blues",
        title="Top categorías por tasa de compra"
    )
    fig_cat.update_layout(template="plotly_white", height=400, xaxis=dict(tickangle=45))

    # =======================
    # Alertas ejecutivas
    # =======================
    avg_interactions = df_patrones["total_interactions"].mean()
    max_day = df_patrones.sort_values("total_interactions", ascending=False).iloc[0]
    min_day = df_patrones.sort_values("total_interactions").iloc[0]

    alerts = dbc.Card(
        dbc.CardBody([
            html.H5(" Alertas ejecutivas", className="card-title"),
            html.Ul([
                html.Li(f"🔺 Día pico: {max_day['tiempo']} con {max_day['total_interactions']:,} interacciones"),
                html.Li(f"🔻 Día mínimo: {min_day['tiempo']} con {min_day['total_interactions']:,} interacciones"),
                html.Li(f" Promedio semanal: {avg_interactions:,.0f} interacciones"),
            ])
        ]),
        className="shadow-sm border-0 bg-light"
    )

    # =======================
    # Layout
    # =======================
    return dbc.Container(
        [
            dbc.Row([
                dbc.Col(kpi1.display(), xs=12, md=2),
                dbc.Col(kpi2.display(), xs=12, md=2),
                dbc.Col(kpi3.display(), xs=12, md=2),
                dbc.Col(kpi4.display(), xs=12, md=3),
                dbc.Col(kpi5.display(), xs=12, md=3),
            ], className="mb-4 g-3"),

            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_trend), xs=12, md=7),
                dbc.Col(dcc.Graph(figure=fig_cat), xs=12, md=5),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(alerts, xs=12),
            ])
        ],
        fluid=True,
    )
