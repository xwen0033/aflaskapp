from dash import html

footer = html.Footer(
    html.P("Copyright © 2023 My Dash WebApp."),
    style={"text-align": "center", "padding": "10px", "background-color": "#f8f9fa"},
)


def get_footer():
    return html.Div("Header Content")