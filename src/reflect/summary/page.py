import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


PAGE_PREFIX = "summary"

layout = html.Div(
    children=[
        dcc.Location(id=f'{PAGE_PREFIX}-url'),
        html.Br(),
        html.Div(id=f"{PAGE_PREFIX}-words"),
    ],
)
