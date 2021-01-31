from dash.dependencies import Output, Input
import funcy as fn

from reflect.app import app
from reflect.utils import _get_query_params
from reflect.summary.page import PAGE_PREFIX


@app.callback(
    Output(component_id=f"{PAGE_PREFIX}-back-button", component_property="href"),
    [Input(component_id=f"{PAGE_PREFIX}-url", component_property="href")],
)
def make_back_button(url: str) -> str:
    params = _get_query_params(url)
    if "project" in params.keys():
        return f"/project?name={fn.first(params['project'])}"
