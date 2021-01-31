from typing import Union, Dict, List

import dash
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import funcy as fn

from reflect.app import app
from reflect.project.page import PAGE_PREFIX
from reflect.config import AppConfig
from reflect.database.mysql import reflectdb, Entry


def create_elements(existing: List[Entry], colour: str) -> List[dbc.ListGroupItem]:
    return [
        dbc.ListGroupItem(
            children=[v.text, html.Div("👍️", style={"float": "right"})],
            style={"border": f"1px solid {colour}"}
        ) for v in existing
    ]


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-great-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-wonder-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-bad-list', component_property='children'),
    ],
    [
        Input(component_id=f"{PAGE_PREFIX}-refresh", component_property="n_intervals"),
        Input(component_id=f"{PAGE_PREFIX}-name", component_property="children")
    ],
)
def get_entries(interval: int, project_name: str):
    entries = reflectdb.get_all_entries_for_project(project_name)
    return (
        create_elements(fn.filter(lambda x: x.type == "GOOD", entries), AppConfig.colour.good),
        create_elements(fn.filter(lambda x: x.type == "WONDERING", entries), AppConfig.colour.wondering),
        create_elements(fn.filter(lambda x: x.type == "BAD", entries), AppConfig.colour.bad)
    )



@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-great-input', component_property='value'),
    [
        Input(component_id=f'{PAGE_PREFIX}-great-submit', component_property='n_clicks'),
        Input(component_id=f"{PAGE_PREFIX}-great-input", component_property="n_submit"),
        Input(component_id=f"{PAGE_PREFIX}-name", component_property="children")
    ],
    [
        State(component_id=f"{PAGE_PREFIX}-great-input", component_property="value")
    ]
)
def add_to_great(save: int, submit: int, project_name: str, value: str):
    if save or submit:
        if value not in (None, ""):
            reflectdb.add_entry(project_name, value, "GOOD")
    return None


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-wonder-input', component_property='value'),
    [
        Input(component_id=f'{PAGE_PREFIX}-wonder-submit', component_property='n_clicks'),
        Input(component_id=f"{PAGE_PREFIX}-wonder-input", component_property="n_submit"),
        Input(component_id=f"{PAGE_PREFIX}-name", component_property="children"),
    ],
    [
        State(component_id=f"{PAGE_PREFIX}-wonder-input", component_property="value"),
    ]
)
def add_to_wonder(save: int, submit: int, project_name: str, value: str):
    if save or submit:
        if value not in (None, ""):
            reflectdb.add_entry(project_name, value, "WONDERING")
    return None


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-bad-input', component_property='value'),
    [
        Input(component_id=f'{PAGE_PREFIX}-bad-submit', component_property='n_clicks'),
        Input(component_id=f"{PAGE_PREFIX}-bad-input", component_property="n_submit"),
        Input(component_id=f"{PAGE_PREFIX}-name", component_property="children")
    ],
    [
        State(component_id=f"{PAGE_PREFIX}-bad-input", component_property="value"),
    ]
)
def add_to_bad(save: int, submit: int, project_name: str, value: Union[None, List[Dict]]):
    if save or submit:
        if value not in (None, ""):
            reflectdb.add_entry(project_name, value, "BAD")
    return None
