from dash.dependencies import Output, Input
import reflect

from reflect.app import app
from reflect.about.page import PAGE_PREFIX


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-version', component_property='children'),
    [Input(component_id=f'{PAGE_PREFIX}-url', component_property='n_clicks')],
)
def get_version(url: int):
    return reflect.__version__
