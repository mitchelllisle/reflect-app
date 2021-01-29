import dash
from dash.dependencies import Output, Input

from src.app import app
from src.create_project.page import PAGE_PREFIX


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-name', component_property='value'),
        Output(component_id=f'{PAGE_PREFIX}-generate-name', component_property='children'),
    ],
    [Input(component_id=f'{PAGE_PREFIX}-generate-name', component_property='n_clicks')],
)
def generate_name(button: int):
    if button:
        return "orderly-numbat", "Generate Another"
    else:
        return dash.no_update, dash.no_update
