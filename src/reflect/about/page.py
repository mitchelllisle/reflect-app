from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html

from reflect.config import AppConfig


PAGE_PREFIX = "about"

layout = html.Div([
    dcc.Location(id=f'{PAGE_PREFIX}-url'),
    html.Img(src=AppConfig.assets.logo, style={"width": "60px", "height": "60px"}),
    html.Br(),
    html.Br(),
    html.B("App Version"),
    html.H1(id=f"{PAGE_PREFIX}-version"),
    html.Br(),
    html.Div(children=[
        html.B("Released"),
        html.P(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        ]
    )
])
