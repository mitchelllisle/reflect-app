from dash.dependencies import Output, Input
import funcy as fn

from reflect.app import app
from reflect.project.page import PAGE_PREFIX
from reflect.utils import _get_query_params


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-refresh', component_property='disabled'),
    [Input(component_id=f'{PAGE_PREFIX}-live-updates', component_property='on')],
)
def live_updates(on: bool):
    if on:
        return False
    else:
        return True



@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-name', component_property='children'),
    [Input(component_id=f'{PAGE_PREFIX}-url', component_property='href')],
)
def get_project(url: str):
    if url:
        params = _get_query_params(url)
        if "name" in params.keys():
            return fn.first(params["name"])


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-summarise', component_property='href'),
    [Input(component_id=f'{PAGE_PREFIX}-name', component_property='children')],
)
def make_summarise_url(name: str):
    return f"/summary?project={name}"
