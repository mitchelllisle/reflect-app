from typing import List, Tuple, Dict, Union
from collections import Counter
import re

import dash
from dash.dependencies import Output, Input
import dash_html_components as html
from sklearn.feature_extraction import _stop_words
import dash_bootstrap_components as dbc
import funcy as fn

from reflect.app import app
from reflect.config import AppConfig
from reflect.summary.page import PAGE_PREFIX
from reflect.database.mysql import reflectdb, Entry
from reflect.utils import _get_query_params

NOT_WORD_OR_DIGIT_EXPR = re.compile(r"([^\d\w\s])")

HeadingForType = fn.partial(html.H1, style={"font-weight": "bold", "padding-right": "20px"})

sort_by_votes = fn.partial(sorted, key=lambda x: _int_or_zero(x.votes), reverse=True)


def clean_and_clount_text(entries: List[str]) -> List[Tuple[str, int]]:
    texts = fn.pluck_attr("text", entries)
    cleaner = fn.rcompose(
        lambda s: s.lower(),
        lambda s: s.strip(),
        lambda s: NOT_WORD_OR_DIGIT_EXPR.sub("", s),
        lambda s: s.split(),
        lambda s: fn.flatten(s)
    )
    cleaned = fn.flatten(fn.map(cleaner, texts))
    valid_words = fn.lfilter(lambda x: x not in _stop_words.ENGLISH_STOP_WORDS, cleaned)
    return Counter(valid_words).most_common(7)


def most_common_words_cards(_type: str, words: List[str] = None):
    word_badges = [
        html.H4(
            dbc.Badge(
                children=[word, dbc.Badge(count, color="light", className="ml-2")],
                pill=True,
                style={"background": AppConfig.colour[_type.lower()]}
            ),
            className="ml-2"
        ) for word, count in words
    ]
    return dbc.Col([
        dbc.Row(
            children=[
                HeadingForType(f"{AppConfig.assets[_type.lower()]} {_type.capitalize()}"),
            ],
        ),
        dbc.Row(word_badges),
    ])


def generate_most_common_words(groups: Dict[str, List[Entry]]) -> dbc.Row:
    cleaned_entries = fn.walk_values(clean_and_clount_text, groups)
    cards = fn.lmap(lambda x: most_common_words_cards(*x), list(cleaned_entries.items()))
    return dbc.Row(cards)


def _int_or_zero(v: Union[int, None]) -> int:
    """
    Used for sorting where you have values that are `None` or other types.
    Make sure your types are ints otherwise everything will be zero (I.E if you have
    ints represented as strings)
    Args:
        v: Value to check

    Returns: Passed integer value or 0

    """
    if isinstance(v, int):
        return v
    else:
        return 0


def generate_ordered_entries(groups: Dict[str, List[Entry]]) -> dbc.Row:
    sorted_groups = fn.walk_values(lambda group: sort_by_votes(group), groups)
    only_votes = fn.walk_values(lambda group: fn.lfilter(lambda x: x.votes is not None, group), sorted_groups)
    items = fn.walk_values(
        lambda group: [
            dbc.ListGroupItem([
                dbc.Badge(
                    f"{item.votes} votes",
                    className="mr-1",
                    style={"background": AppConfig.colour[item.type.lower()]}
                ),
                item.text
            ]) for item in group
        ],
        only_votes
    )
    columns = fn.lmap(
        lambda x: dbc.Col(
            [html.B(x[0].capitalize(), style={"margin-left": "15px"}), dbc.Col(x[1])]
        ), items.items()
    )
    return dbc.Row(columns)


@app.callback(
    [
        Output(component_id=f"{PAGE_PREFIX}-words", component_property="children"),
        Output(component_id=f"{PAGE_PREFIX}-sorted-entries", component_property="children")
    ],
    [Input(component_id=f"{PAGE_PREFIX}-url", component_property="href")],
)
def calculate_word_counts(url: str) -> Tuple[html.Div, html.Div]:
    params = _get_query_params(url)
    if "project" in params.keys():
        entries = reflectdb.get_all_entries_for_project(fn.first(params["project"]))
        groups = fn.group_by(lambda x: x.type, entries)
        most_common = generate_most_common_words(groups)
        sorted_entries = generate_ordered_entries(groups)
        return most_common, sorted_entries
    else:
        return dash.no_update, dash.no_update
