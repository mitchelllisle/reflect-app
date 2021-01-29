from urllib.parse import parse_qs, urlparse
from typing import Dict

from dash.dependencies import Output, Input, State
import funcy as fn

from src.app import app
from src.project.page import PAGE_PREFIX


@app.callback(
    Output(f"{PAGE_PREFIX}-timer-modal", "is_open"),
    [
        Input(f"{PAGE_PREFIX}-timer", "n_clicks"),
        Input(f"{PAGE_PREFIX}-timer-close", "n_clicks")
    ],
    [State(f"{PAGE_PREFIX}-timer-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open