import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from reflect.config import AppConfig
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
                        daq.NumericInput(
                          id=f'{PAGE_PREFIX}-timer-length',
                          min=0,
                          max=10,
                          value=0
                        ),
                    ],
                    style={"width": "auto", "margin-left": "auto", "margin-right": "auto"}
                ),
                dbc.ModalFooter([
                    dbc.Button("Start", id=f"{PAGE_PREFIX}-timer-start-button", color="primary"),
                    dbc.Button("Close", id=f"{PAGE_PREFIX}-timer-close-button", color="danger")
                ]),
            ],
            id=f"{PAGE_PREFIX}-timer-modal",
        ),
    ]
)

layout = html.Div([
    dcc.Location(id=f'{PAGE_PREFIX}-url'),
    dcc.Interval(id=f"{PAGE_PREFIX}-refresh", interval=10000, disabled=True),
    dcc.Interval(id=f"{PAGE_PREFIX}-timer-refresh", interval=1000, disabled=True),
    html.Span(id=f"{PAGE_PREFIX}-timer-start", style={"display": "none"}),
    html.Span(id=f"{PAGE_PREFIX}-timer-end", style={"display": "none"}),
    modal,
    html.Br(),
    dbc.Row([
        html.Span(id=f"{PAGE_PREFIX}-id", style={"display": "none"}),
        dbc.Col(html.H1(id=f"{PAGE_PREFIX}-name", style={"font-weight": "bold", "font-size": "50px"})),
        dbc.Col(
            dbc.Button(
                "Go to Summary",
                id=f"{PAGE_PREFIX}-summarise",
                outline=False,
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
    html.H2(id=f"{PAGE_PREFIX}-timer-pretty"),
    html.Span(id=f"{PAGE_PREFIX}-timer-countdown", style={"display": "none"}),
    html.Br(),
    dbc.Row(
        children=[
            daq.BooleanSwitch(
                id=f'{PAGE_PREFIX}-live-updates',
                on=False,
                style={"margin-left": "10px"},
            ),
            html.B("Live Updates", style={"margin-left": "5px"})
        ]
    ),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            children=[
                html.H3(f"{AppConfig.assets.good} It was great that...", style={"font-weight": "bold"}),
                dbc.InputGroup([
                    dbc.Input(id=f"{PAGE_PREFIX}-great-input", placeholder="..."),
                    dbc.Button(id=f"{PAGE_PREFIX}-great-submit", children="⮑", color="#FFF"),
                ]),
                html.Br(),
                dbc.ListGroup(id=f"{PAGE_PREFIX}-great-list")
            ],
        ),
        dbc.Col(
            children=[
                html.H3(f"{AppConfig.assets.wondering} I'm wondering about...", style={"font-weight": "bold"}),
                dbc.InputGroup([
                    dbc.Input(id=f"{PAGE_PREFIX}-wonder-input", placeholder="..."),
                    dbc.Button(id=f"{PAGE_PREFIX}-wonder-submit", children="⮑", color="#FFF")
                ]),
                html.Br(),
                dbc.ListGroup(id=f"{PAGE_PREFIX}-wonder-list")
            ],
        ),
        dbc.Col(
            children=[
                html.H3(f"{AppConfig.assets.bad} It wasn't so great that...", style={"font-weight": "bold"}),
                dbc.InputGroup([
                    dbc.Input(id=f"{PAGE_PREFIX}-bad-input", placeholder="..."),
                    dbc.Button(id=f"{PAGE_PREFIX}-bad-submit", children="⮑", color="#FFF")
                ]),
                html.Br(),
                dbc.ListGroup(id=f"{PAGE_PREFIX}-bad-list", flush=True)
            ],
        ),
    ]),
    html.Br(),
])
