from random import choice

import dash
from dash.dependencies import Output, Input

from reflect.app import app
from reflect.create_project.page import PAGE_PREFIX
from reflect.config import AppConfig


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-name', component_property='value'),
        Output(component_id=f'{PAGE_PREFIX}-generate-name', component_property='children'),
    ],
    [Input(component_id=f'{PAGE_PREFIX}-generate-name', component_property='n_clicks')],
)
def generate_name(button: int):
    if button:
        generated_name = f"{choice(AppConfig.semantic_naming.adjectives)}-{choice(AppConfig.semantic_naming.animals)}"
        return generated_name, "Generate Another"
    else:
        return dash.no_update, dash.no_update
