import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


PAGE_PREFIX = "summary"

layout = html.Div(
    children=[
        dcc.Location(id=f'{PAGE_PREFIX}-url'),
        html.A("< Back", id=f"{PAGE_PREFIX}-back-button"),
        html.Br(),
        html.Br(),
        dbc.Card([
            dbc.CardHeader(
                children=html.B("Most Common Words by Type", style={"font-size": "20px"}),
                style={"border": "0px", "background": "white"}
            ),
            dcc.Loading(dbc.CardBody(id=f"{PAGE_PREFIX}-words", style={"padding": "5%"}), type="dot")
        ]),
        html.Br(),
        dbc.Card([
            dbc.CardHeader(
                children=html.B("Most Votes", style={"font-size": "20px"}),
                style={"border": "0px", "background": "white"}
            ),
            dcc.Loading(dbc.CardBody(id=f"{PAGE_PREFIX}-sorted-entries"), type="dot")
        ])
    ],
)
