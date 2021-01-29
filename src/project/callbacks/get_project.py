from urllib.parse import parse_qs, urlparse
from typing import Dict

from dash.dependencies import Output, Input
import funcy as fn

from src.app import app
from src.project.page import PAGE_PREFIX


def _get_query_params(url: str) -> Dict:
    return parse_qs(urlparse(url).query)


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-name', component_property='children'),
    [Input(component_id=f'{PAGE_PREFIX}-url', component_property='href')],
)
def get_project(url: str):
    if url:
        params = _get_query_params(url)
        return fn.first(params["name"])
