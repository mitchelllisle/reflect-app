from typing import NewType
import re

from dash.dependencies import Output, Input
from funcy import rcompose

from src.app import app
from src.create_project.page import PAGE_PREFIX

ProjectName = NewType("ProjectName", str)

PUNCTUATION_EXPR = re.compile(r"([\s]+)|([^\-\w\d])+")


def clean_up_name(name: str) -> ProjectName:
    clean = rcompose(
        lambda s: s.strip(),
        lambda s: s.lower(),
        lambda s: PUNCTUATION_EXPR.sub("-", s),
        lambda s: re.sub(r"(-{2,})", "-", s)
    )
    cleaned = clean(name)
    return ProjectName(cleaned)


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-save', component_property='href'),
    [Input(component_id=f'{PAGE_PREFIX}-name', component_property='value')],
)
def create_project(name: str):
    if name:
        cleaned = clean_up_name(name)
        return f"/project?name={cleaned}"
