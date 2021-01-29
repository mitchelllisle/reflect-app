import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from src.navbar import navbar

app = dash.Dash(
    __name__,
    title="Reflect",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.COSMO],
    update_title=False
)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='app-page-content', style={"margin-left": "5%", "margin-right": "5%"})
])
