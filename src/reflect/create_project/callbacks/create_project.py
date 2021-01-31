from typing import NewType
import re

import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from funcy import rcompose
from mysql.connector.errors import IntegrityError

from reflect.app import app
from reflect.create_project.page import PAGE_PREFIX
from reflect.database.mysql import reflectdb

ProjectName = NewType("ProjectName", str)

PUNCTUATION_EXPR = re.compile(r"([\s]+)|([^\-\w\d])+")


def clean_up_name(name: str) -> ProjectName:
    clean = rcompose(
        lambda s: s.strip(),
        lambda s: s.lower(),
        lambda s: PUNCTUATION_EXPR.sub("-", s),
        lambda s: re.sub(r"(-{2,})", "-", s)
    )
    cleaned = clean(name)
    return ProjectName(cleaned)


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-save', component_property='href'),
        Output(component_id=f'{PAGE_PREFIX}-save', component_property='disabled'),
        Output(component_id=f'{PAGE_PREFIX}-error', component_property='children')
    ],
    [
        Input(component_id=f'{PAGE_PREFIX}-name', component_property='value'),
        Input(component_id=f'{PAGE_PREFIX}-save', component_property='n_clicks')
    ],
)
def create_project(name: str, save: int):
    if name:
        cleaned = clean_up_name(name)
        try:
            if reflectdb.check_project_name(name) is not None:
                raise IntegrityError(f"project with name {name} already exists")
            if save:
                reflectdb.save_project(cleaned)
            return f"/project?name={cleaned}", False, dash.no_update
        except IntegrityError as err:
            return dash.no_update, True, dbc.Alert(
                children="Project name already exists. Please choose another",
                color="warning",
                duration=3000
            )
        except Exception as err:
            return dash.no_update, True, dbc.Alert(
                children=f"Unable to create project due to error type: {err.__class__.__name__}",
                color="warning", duration=3000
            )
    else:
        raise PreventUpdate()
