from typing import List, Tuple
from collections import Counter
import re

from dash.dependencies import Output, Input
import dash_html_components as html
from sklearn.feature_extraction import _stop_words
import dash_bootstrap_components as dbc
import funcy as fn

from reflect.app import app
from reflect.config import AppConfig
from reflect.summary.page import PAGE_PREFIX
from reflect.database.mysql import reflectdb
from reflect.utils import _get_query_params

NOT_WORD_OR_DIGIT_EXPR = re.compile(r"([^\d\w\s])")


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
    return Counter(valid_words).most_common(5)


def make_cards(_type: str, words: List[str] = None):
    word_badges = [
        dbc.Badge(
            children=[word, dbc.Badge(count, color="light", className="ml-1")],
            className="mr-1",
            style={"background": AppConfig.colour[_type.lower()]}
        ) for word, count in words
    ]
    return dbc.Col([
        dbc.Row(
            children=[
                html.H1(
                    f"{AppConfig.assets[_type.lower()]} {_type.capitalize()}",
                    style={"font-weight": "bold", "padding-right": "20px"}
                ),
            ],
        ),
        dbc.Row(word_badges),
    ])


@app.callback(
    Output(component_id=f"{PAGE_PREFIX}-words", component_property="children"),
    [Input(component_id=f"{PAGE_PREFIX}-url", component_property="href")],
)
def calculate_word_counts(url: str) -> html.Div:
    params = _get_query_params(url)
    if "project" in params.keys():
        entries = reflectdb.get_all_entries_for_project(fn.first(params["project"]))
        groups = fn.group_by(lambda x: x.type, entries)
        cleaned_entries = fn.walk_values(clean_and_clount_text, groups)
        cards = fn.lmap(lambda x: make_cards(*x), list(cleaned_entries.items()))
        return dbc.Row(cards)
