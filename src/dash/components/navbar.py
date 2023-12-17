import dash_bootstrap_components as dbc

navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Seasonality", href="/seasonality")),
        dbc.NavItem(dbc.NavLink("Wave Equation", href="/wave_equation")),
        dbc.NavItem(dbc.NavLink("Weather", href="/weather")),
        dbc.NavItem(dbc.NavLink("Classification", href="/classification")),
    ],
    className="navbar",
)