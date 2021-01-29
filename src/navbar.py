import dash_html_components as html
import dash_bootstrap_components as dbc
from src.config import AppConfig

navbar = dbc.Navbar(
    [
        dbc.Col(html.A(dbc.NavbarBrand("Reflect", style={"font-weight": "bold", "font-size": "30px"}))),
        dbc.Col([
            html.A("About", style={"float": "right", "font-weight": "bold"}),
        ])
    ],
    color="#FFF",
    dark=False,
    style={"margin-left": "3%", "margin-right": "5%"}
)
