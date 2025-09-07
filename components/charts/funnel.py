import plotly.express as px
import pandas as pd

def funnel_chart(df: pd.DataFrame, stages: list[str], values: str, title="Funnel"):
    fig = px.funnel(df, x=values, y=stages, title=title)
    fig.update_layout(template="plotly_white")
    return fig
