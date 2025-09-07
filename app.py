import dash
from dash import html
import dash_bootstrap_components as dbc
from utils.cache import cache
from config import Config

# ==========================
# App principal
# ==========================
app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
    ],
    title="Ecommerce Analytics - Unisabana"
)

server = app.server
cache.init_app(server)

# ==========================
# Navbar superior
# ==========================
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Unisabana - Big Data Ecommerce", href="/"),

            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Inicio", href="/")),
                    dbc.NavItem(dbc.NavLink("Conversiones", href="/conversiones")),
                    dbc.NavItem(dbc.NavLink("Marcas", href="/marcas")),
                    dbc.NavItem(dbc.NavLink("Patrones", href="/patrones")),
                    dbc.NavItem(dbc.NavLink("Usuarios", href="/usuarios")),
                    dbc.NavItem(dbc.NavLink("CLV", href="/clv")),
                ],
                pills=True,
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    className="mb-4"
)

# ==========================
# Layout
# ==========================
app.layout = dbc.Container(
    [
        navbar,
        dash.page_container
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
