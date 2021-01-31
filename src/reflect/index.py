from dash.dependencies import Output, Input
import dash_html_components as html

from reflect.config import AppConfig
from reflect.app import app

from reflect.create_project import page as add_project
from reflect.project import page as project
from reflect.about import page as about
from reflect.summary import page as summary
from reflect.view_projects import page as view_projects


@app.callback(
    Output(component_id='app-page-content', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_page(pathname):
    routes = {
        "/": add_project.layout,
        "/about": about.layout,
        "/project": project.layout,
        "/projects": view_projects.layout,
        "/summary": summary.layout
    }
    try:
        return routes[pathname]
    except KeyError:
        return html.Div(
            children=[
                html.H1("404", style={"font-weight": "bold", "font-size": "100px"}),
                html.H3("Oops! Nothing found here", style={"font-weight": "bold"}),
                html.Img(src=AppConfig.assets.missing, style={"width": "100%"}),
            ],
            style={"margin-left": "auto", "margin-right": "auto"}
        )
