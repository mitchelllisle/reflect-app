from dash.dependencies import Output, Input
import dash_html_components as html

from src.config import AppConfig
from src.app import app
from src.create_project import page as add_project
from src.project import page as project


@app.callback(
    Output(component_id='app-page-content', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_page(pathname):
    routes = {
        "/": add_project.layout,
        "/project": project.layout
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
