from dash import html
import dash_bootstrap_components as dbc

class kpibadge:
    def __init__(self, kpi, label, badgetype):
        self.kpi = kpi
        self.label = label
        self.badgetype = badgetype
        self.color = "danger" if badgetype == "Danger" else "success"

    def display(self):
        return html.Div(
            [
                html.Div(self.label, className="h6"),
                html.H2(self.kpi, className="d-flex justify-content-end"),
                dbc.Badge(self.badgetype, color=self.color, className="mr-1"),
            ],
            className="m-2",
        )
