from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import funcy as fn
from typing import Union, Dict, List

from src.app import app
from src.project.page import PAGE_PREFIX


class Colours:
    good = "#BFEA53"
    wondering = "#FFC666"
    bad = "#F574A2"


def add_to_element(value, existing, colour):
    items = [value]
    if existing:
        children = fn.lmap(lambda x: x["props"]["children"], existing)
        children = fn.lmap(
            lambda x: fn.first(
                fn.lfilter(lambda v: isinstance(v, str), x)
            ),
            children
        )
        items = fn.merge(items, children)

    vals = fn.lfilter(lambda x: fn.notnone(x) and x != "", items)
    return [
        dbc.ListGroupItem(
            children=[v, html.Div("❤️️", style={"float": "right"})],
            style={"border": f"1px solid {colour}"}
        ) for v in fn.distinct(vals)
    ]


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-great-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-great-input', component_property='value'),
    ],
    [Input(component_id=f'{PAGE_PREFIX}-great-submit', component_property='n_clicks')],
    [
        State(component_id=f"{PAGE_PREFIX}-great-input", component_property="value"),
        State(component_id=f"{PAGE_PREFIX}-great-list", component_property="children")
    ]
)
def add_to_great(save: int, value: str, existing: Union[None, List[Dict]]):
    return add_to_element(value, existing, Colours.good), None


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-wonder-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-wonder-input', component_property='value'),
    ],
    [Input(component_id=f'{PAGE_PREFIX}-wonder-submit', component_property='n_clicks')],
    [
        State(component_id=f"{PAGE_PREFIX}-wonder-input", component_property="value"),
        State(component_id=f"{PAGE_PREFIX}-wonder-list", component_property="children")
    ]
)
def add_to_wonder(save: int, value: str, existing: Union[None, List[Dict]]):
    return add_to_element(value, existing, Colours.wondering), None


@app.callback(
    [
        Output(component_id=f'{PAGE_PREFIX}-bad-list', component_property='children'),
        Output(component_id=f'{PAGE_PREFIX}-bad-input', component_property='value'),
    ],
    [Input(component_id=f'{PAGE_PREFIX}-bad-submit', component_property='n_clicks')],
    [
        State(component_id=f"{PAGE_PREFIX}-bad-input", component_property="value"),
        State(component_id=f"{PAGE_PREFIX}-bad-list", component_property="children")
    ]
)
def add_to_bad(save: int, value: str, existing: Union[None, List[Dict]]):
    return add_to_element(value, existing, Colours.bad), None
