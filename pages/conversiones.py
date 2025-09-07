import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from db_connection import load_table
dash.register_page(__name__, path="/conversiones", name="Conversiones")

def layout():
    df_cat = load_table("conversion_categorias")
    df_brand = load_table("top5_reconocidas")

    # =======================
    # Funnel Global (agregado)
    # =======================
    total_views = df_cat["view"].sum()
    total_carts = df_cat["cart"].sum()
    total_purchases = df_cat["purchase"].sum()

    funnel_global = go.Figure(go.Funnel(
        y=["Vistas", "Carritos", "Compras"],
        x=[total_views, total_carts, total_purchases],
        textinfo="value+percent initial"
    ))
    funnel_global.update_layout(title="Funnel Global de Conversión")

    # =======================
    # Top categorías por tasa de compra
    # =======================
    top_cats = df_cat.sort_values("purchase_rate", ascending=False).head(8)
    fig_top_cats = px.bar(
        top_cats,
        x="category_code", y="purchase_rate",
        title="Top Categorías por Tasa de Conversión",
        text_auto=".2%"
    )
    fig_top_cats.update_layout(template="plotly_white", xaxis=dict(tickangle=30))

    # =======================
    # Funnel Marcas (solo top 5)
    # =======================
    funnel_brand = go.Figure()
    for col in ["view", "cart", "purchase"]:
        funnel_brand.add_trace(go.Funnel(
            y=df_brand["brand"],
            x=df_brand[col],
            name=col.capitalize()
        ))
    funnel_brand.update_layout(title="Funnel de Conversión (Top 5 Marcas)")

    # =======================
    # Tabla Resumen (Top 10 categorías)
    # =======================
    summary = df_cat[[
        "category_code", "cart_rate", "purchase_rate", "cart_to_purchase_rate"
    ]].sort_values("purchase_rate", ascending=False).head(10)

    summary_table = dbc.Table.from_dataframe(
        summary.round(3),
        striped=True,
        bordered=True,
        hover=True
    )

    # =======================
    # Layout con Tabs
    # =======================
    return dbc.Container([
        html.H2("Análisis de Conversiones"),

        dcc.Tabs([
            dcc.Tab(label="Funnel Global", children=[
                dcc.Graph(figure=funnel_global)
            ]),
            dcc.Tab(label="Top Categorías", children=[
                dcc.Graph(figure=fig_top_cats),
                html.P("Estas son las categorías con mayor eficiencia de conversión.")
            ]),
            dcc.Tab(label="Funnel Marcas", children=[
                dcc.Graph(figure=funnel_brand)
            ]),
            dcc.Tab(label="Resumen Categorías", children=[
                html.H5("Top 10 Categorías - Tasas de Conversión"),
                summary_table
            ])
        ])
    ], fluid=True)
def update_conversiones(filters):
    df_cat = load_table("conversion_categorias", filters)
    df_brand = load_table("top5_reconocidas", filters)

    fig_cat = px.funnel(df_cat, x="view", y="category_code", color_discrete_sequence=px.colors.qualitative.Set2)
    fig_brand = px.funnel(df_brand, x="view", y="brand", color_discrete_sequence=px.colors.qualitative.Set1)

    return fig_cat, fig_brand
