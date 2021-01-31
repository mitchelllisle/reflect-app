from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_html_components as html

from reflect.app import app
from reflect.view_projects.page import PAGE_PREFIX
from reflect.database.mysql import reflectdb


@app.callback(
    Output(component_id=f'{PAGE_PREFIX}-list', component_property='children'),
    [Input(component_id=f'{PAGE_PREFIX}-url', component_property='n_clicks')],
)
def get_existing_projects(url: int):
    projects = reflectdb.get_all_projects()
    return dbc.ListGroup(
        [
            dbc.ListGroupItem(
            html.A(
                children=[
                    html.B(f"{project.name}"),
                    dbc.FormText(f"Created: {project.created_at}")
                ],
                href=f"/project?name={project.name}"
            )
        ) for project in projects]
    )
