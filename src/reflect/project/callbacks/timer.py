import datetime as dt
import re

import dash
from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_bootstrap_components as dbc

from reflect.app import app
from reflect.config import AppConfig
from reflect.project.page import PAGE_PREFIX


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
TIME_DELTA_EXPR = re.compile(r"(?:^\d:+?(?=\d))(\d+:\d+)(?:.\d+$)")


@app.callback(
    Output(f"{PAGE_PREFIX}-timer-modal", "is_open"),
    [
        Input(f"{PAGE_PREFIX}-timer", "n_clicks"),
        Input(f"{PAGE_PREFIX}-timer-start-button", "n_clicks"),
        Input(f"{PAGE_PREFIX}-timer-close-button", "n_clicks")
    ],
    [State(f"{PAGE_PREFIX}-timer-modal", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open


@app.callback(
    [
        Output(f"{PAGE_PREFIX}-timer-countdown", "children"),
        Output(f"{PAGE_PREFIX}-timer-pretty", "children"),
        Output(f"{PAGE_PREFIX}-timer-refresh", "disabled"),
    ],
    [
        Input(f"{PAGE_PREFIX}-timer-refresh", "n_intervals"),
        Input(f"{PAGE_PREFIX}-timer-start", "children"),
        Input(f"{PAGE_PREFIX}-timer-end", "children")
    ],
    [
        State(f"{PAGE_PREFIX}-timer-countdown", "children")
    ],
)
def update_timer(_, start, end, countdown):
    if start:
        if countdown:
            now = dt.datetime.now()
            delta = dt.datetime.strptime(end, DATE_FORMAT) - now
            if delta.total_seconds() > 0:
                return now, f"⏲ {TIME_DELTA_EXPR.search(str(delta)).group(1)}", False
            else:
                return (
                    now,
                    dbc.Row([
                        html.P("🎉 Timer Finished", style={'margin-top': 'none', 'margin-left': '12px'}),
                        html.Img(
                            src=AppConfig.assets.bean,
                            width=50,
                            height=67
                        ),
                    ]),
                    True
                )
        else:
            _start = dt.datetime.strptime(start, DATE_FORMAT)
            delta = dt.datetime.strptime(end, DATE_FORMAT) - dt.datetime.now()
            return _start, f"⏲ {TIME_DELTA_EXPR.search(str(delta)).group(1)}", False
    else:
        return dash.no_update, dash.no_update, dash.no_update


@app.callback(
    [
        Output(f"{PAGE_PREFIX}-timer-start", "children"),
        Output(f"{PAGE_PREFIX}-timer-end", "children"),
    ],
    [Input(f"{PAGE_PREFIX}-timer-start-button", "n_clicks")],
    [State(f'{PAGE_PREFIX}-timer-length', "value")],
    prevent_initial_callback=True
)
def update_timer_bounds(submit: int, length: int):
    if submit:
        start = dt.datetime.now()
        return start, start + dt.timedelta(minutes=length)
    else:
        return dash.no_update, dash.no_update
