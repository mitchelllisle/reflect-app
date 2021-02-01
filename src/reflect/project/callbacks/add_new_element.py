from typing import List

import dash
from dash.dependencies import Output, Input, State, MATCH
import dash_bootstrap_components as dbc
import dash_html_components as html
import funcy as fn

from reflect.app import app
from reflect.project.page import PAGE_PREFIX
from reflect.config import AppConfig
from reflect.database.mysql import reflectdb, Entry
from reflect.utils import get_triggered_component


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
        State(component_id={"type": "entry-display", "index": MATCH}, component_property="id")
    ]
)
def update_vote(clicks: int, project: str, entry: str):
    entry_id = fn.get_in(entry, ["index"])
    if clicks:
        reflectdb.save_vote(project, entry_id)
        votes = reflectdb.get_votes(entry_id)
        return f"👍 {votes.amount}"
    else:
        return dash.no_update


def save_entry(save: int, submit: int, value: str, project_name: str, _type: str):
    if save or submit:
        if value not in (None, ""):
            reflectdb.add_entry(project_name, value, _type)


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-great-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-wonder-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-bad-list', component_property='children'),
    ],
    [
        Input(component_id=f"{PAGE_PREFIX}-refresh", component_property="n_intervals"),
        Input(component_id=f"{PAGE_PREFIX}-name", component_property="children"),
        Input(component_id=f'{PAGE_PREFIX}-great-submit', component_property='n_clicks'),
        Input(component_id=f"{PAGE_PREFIX}-great-input", component_property="n_submit"),
        Input(component_id=f'{PAGE_PREFIX}-wonder-submit', component_property='n_clicks'),
        Input(component_id=f"{PAGE_PREFIX}-wonder-input", component_property="n_submit"),
        Input(component_id=f'{PAGE_PREFIX}-bad-submit', component_property='n_clicks'),
        Input(component_id=f"{PAGE_PREFIX}-bad-input", component_property="n_submit"),
    ],
    [
        State(component_id=f"{PAGE_PREFIX}-great-input", component_property="value"),
        State(component_id=f"{PAGE_PREFIX}-wonder-input", component_property="value"),
        State(component_id=f"{PAGE_PREFIX}-bad-input", component_property="value")
    ]
)
def get_entries(
        interval: int, project_name: str,
        great_submit: int, great_input: int,
        wonder_submit: int, wonder_input: int,
        bad_submit: int, bad_input: int,
        great_value: str, wonder_value: str, bad_value: str
):
    triggered_by = get_triggered_component()
    if triggered_by.startswith("project-great"):
        save_entry(great_submit, great_input, great_value, project_name, "GOOD")
    elif triggered_by.startswith("project-wonder"):
        save_entry(wonder_submit, wonder_input, wonder_value, project_name, "WONDERING")
    elif triggered_by.startswith("project-bad"):
        save_entry(bad_submit, bad_input, bad_value, project_name, "BAD")
    entries = reflectdb.get_all_entries_for_project(project_name)
    return (
        create_elements(fn.filter(lambda x: x.type == "GOOD", entries), AppConfig.colour.good),
        create_elements(fn.filter(lambda x: x.type == "WONDERING", entries), AppConfig.colour.wondering),
        create_elements(fn.filter(lambda x: x.type == "BAD", entries), AppConfig.colour.bad)
    )
