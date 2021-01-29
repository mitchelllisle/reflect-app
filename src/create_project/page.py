import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import funcy as fn
from src.config import AppConfig


PAGE_PREFIX = "add-project"


layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Input(
            id=f"{PAGE_PREFIX}-name",
            style={"width": "30%"},
            placeholder="Enter project name...",
        ),
        dbc.Button(
            id=f"{PAGE_PREFIX}-save",
            children="Create",
            external_link=True,
            style={
                "background-color": AppConfig.colour.primary,
                "color": AppConfig.colour.dark,
                "border": "0px",
                "min-width": "200px"
            }
        )
    ]),
    dbc.Row([
        dbc.Button("Generate one for me", id=f"{PAGE_PREFIX}-generate-name", color="link", style={"padding-left": "0"})
    ]),
    html.Br(),
])
