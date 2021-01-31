import dash_core_components as dcc
import dash_html_components as html


PAGE_PREFIX = "view-project"

layout = html.Div([
    dcc.Location(id=f'{PAGE_PREFIX}-url'),
    html.Br(),
    html.Div(id=f"{PAGE_PREFIX}-list")
])
