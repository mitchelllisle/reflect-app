import dash_html_components as html
import dash_bootstrap_components as dbc
from reflect.config import AppConfig


PAGE_PREFIX = "add-project"


layout = html.Div(
    children=[
        html.Br(),
        dbc.InputGroup([
            dbc.Input(
                id=f"{PAGE_PREFIX}-name",
                placeholder="Enter project name...",
                style={
                    "width": "30%",
                    "height": "100px",
                    "font-size": "50px"
                },
            ),
            dbc.Button(
                id=f"{PAGE_PREFIX}-save",
                children="Create",
                external_link=True,
                disabled=True,
                style={
                    "background-color": AppConfig.colour.primary,
                    "color": AppConfig.colour.dark,
                    "border": "0px",
                    "width": "200px",
                    "font-size": "20px"
                }
            )
        ]),
        dbc.Button(
            "Generate one for me",
            id=f"{PAGE_PREFIX}-generate-name",
            color="link",
            style={"padding-left": "0"}
        ),
        html.Br(),
        html.Div(id=f"{PAGE_PREFIX}-error")
    ],
    style={"margin-left": "10%", "margin-right": "10%", "padding-top": "15%"}
)
