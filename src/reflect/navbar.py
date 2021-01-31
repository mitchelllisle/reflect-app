import dash_html_components as html
import dash_bootstrap_components as dbc
import funcy as fn

NavLink = fn.partial(
    html.A,
    style={"float": "right", "color": "black", "font-weight": "bold", "padding-left": "20px"}
)

navbar = dbc.Navbar(
    [
        dbc.Col(html.A(dbc.NavbarBrand("Reflect", href="/", style={"font-weight": "bold", "font-size": "30px"}))),
        NavLink("Projects", href="/projects"),
        NavLink("About", href="/about")
    ],
    color="transparent",
    dark=False,
    style={"margin-left": "3%", "margin-right": "5%"}
)
