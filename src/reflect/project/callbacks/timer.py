import time
import datetime as dt
import re

import dash
from dash.dependencies import Output, Input, State
import funcy as fn

from reflect.app import app
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
def update_timer(refresh, start, end, countdown):
    if start:
        if countdown:
            now = dt.datetime.now()
            parsed = dt.datetime.strptime(countdown, DATE_FORMAT)
            delta = dt.datetime.strptime(end, DATE_FORMAT) - now
            if delta.total_seconds() > 0:
                return now, f"⏲ {TIME_DELTA_EXPR.search(str(delta)).group(1)}"
            else:
                return now, "🎉 Timer Finished"
        else:
            _start = dt.datetime.strptime(start, DATE_FORMAT)
            delta = dt.datetime.strptime(end, DATE_FORMAT) - dt.datetime.now()
            return _start, f"⏲ {TIME_DELTA_EXPR.search(str(delta)).group(1)}"
    else:
        return dash.no_update, dash.no_update


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
