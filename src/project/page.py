import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from src.config import AppConfig
import dash_daq as daq


PAGE_PREFIX = "project"

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Set Timer"),
                dbc.ModalBody(html.H6("Chose how long you want the timer to run")),
                dbc.ModalBody(
                    children=[
                        daq.Knob(
                          id=f'{PAGE_PREFIX}-timer-length',
                          min=0,
                          max=10,
                          value=3
                        ),
                    ],
                    style={"width": "auto", "margin-left": "auto", "margin-right": "auto"}
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id=f"{PAGE_PREFIX}-timer-close", className="ml-auto")
                ),
            ],
            id=f"{PAGE_PREFIX}-timer-modal",
        ),
    ]
)

layout = html.Div([
    dcc.Location(id=f'{PAGE_PREFIX}-url'),
    modal,
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1(id=f"{PAGE_PREFIX}-name", style={"font-weight": "bold", "font-size": "50px"})),
        dbc.Col(
            dbc.Button(
                "Go to Summary",
                style={
                    "float": "right",
                    "height": "40px",
                    "width": "140px",
                    "border": "0px",
                    "color": "black",
                    "background-color": AppConfig.colour.orange
                }
            )
        ),
    ]),
    dbc.Button("Start Timer", id=f"{PAGE_PREFIX}-timer", color="link", style={"padding-left": "0px"}),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            children=[
                html.H3("😀 It was great that...", style={"font-weight": "bold"}),
                dbc.InputGroup([
                    dbc.Input(id=f"{PAGE_PREFIX}-great-input", placeholder="..."),
                    dbc.Button(id=f"{PAGE_PREFIX}-great-submit", children="Submit"),
                ]),
                html.Br(),
                dbc.ListGroup(id=f"{PAGE_PREFIX}-great-list")
            ],
        ),
        dbc.Col(
            children=[
                html.H3("🤔 I'm wondering about...", style={"font-weight": "bold"}),
                dbc.InputGroup([
                    dbc.Input(id=f"{PAGE_PREFIX}-wonder-input", placeholder="..."),
                    dbc.Button(id=f"{PAGE_PREFIX}-wonder-submit", children="Submit")
                ]),
                html.Br(),
                dbc.ListGroup(id=f"{PAGE_PREFIX}-wonder-list")
            ],
        ),
        dbc.Col(
            children=[
                html.H3("😓 It wasn't so great that...", style={"font-weight": "bold"}),
                dbc.InputGroup([
                    dbc.Input(id=f"{PAGE_PREFIX}-bad-input", placeholder="..."),
                    dbc.Button(id=f"{PAGE_PREFIX}-bad-submit", children="Submit")
                ]),
                html.Br(),
                dbc.ListGroup(id=f"{PAGE_PREFIX}-bad-list", flush=True)
            ],
        ),
    ]),
    html.Br(),
])
