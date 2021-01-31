from typing import Union, Dict, List

import dash
from dash.dependencies import Output, Input, State, MATCH
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
            children=[
                dbc.Button(v.text, id={"type": "entry-display", "index": v.id}, color="link"),
                html.Div(
                    f"👍 {0 if v.votes is None else v.votes}",
                    id={"type": "like-counter", "index": v.id},
                    style={"float": "right"})
            ],
            style={"border": f"1px solid {colour}"}
        ) for v in existing
    ]


@app.callback(
    Output(component_id={"type": "like-counter", "index": MATCH}, component_property='children'),
    [
        Input(component_id={"type": "entry-display", "index": MATCH}, component_property="n_clicks"),
    ],
    [
        State(component_id=f"{PAGE_PREFIX}-name", component_property="children"),
        State(component_id={"type": "entry-display", "index": MATCH}, component_property="id")]
)
def update_vote(clicks: int, project: str, entry: str):
    if clicks:
        entry_id = fn.get_in(entry, ["index"])
        reflectdb.save_vote(project, entry_id)
    return dash.no_update


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
