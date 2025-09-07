from dash import html
import dash_bootstrap_components as dbc

class kpicard:
    """
    KPI Card component for executive dashboards.
    Displays a title, value, optional subtitle, and an icon.
    """

    def __init__(self, value: str, title: str, subtitle: str = "", icon: str = "bi-bar-chart", color: str = "primary"):
        self.value = value
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.color = color

    def display(self):
        return dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.I(className=f"bi {self.icon} me-2", style={"fontSize": "1.5rem", "color": self.color}),
                    html.Span(self.title, className="fw-bold"),
                ], className="d-flex align-items-center mb-2"),
                html.H3(self.value, className="card-title"),
                html.Small(self.subtitle, className="text-muted")
            ]),
            className="shadow-sm"
        )
