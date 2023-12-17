""" initializes the Dash app, sets up the layout, and runs the server"""

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from src.dash.components.footer import footer
from src.dash.components.navbar import navbar
from pages import home, wave_equation, weather, seasonality, classification

app = Dash(__name__)

# Define page layouts
# Set the initial layout dynamically within the callback
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Div(id="page-content"),  # Placeholder for page content
        footer
    ]
)


# Define callbacks to switch between pages
@app.callback(
    [Output("page-content", "children")],
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/wave_equation":
        return [wave_equation.get_layout()]
    elif pathname == "/seasonality":
        return [seasonality.get_layout()]
    elif pathname == "/weather":
        return [weather.get_layout()]
    elif pathname == "/classification":
        return [classification.get_layout()]
    else:
        return [home.get_layout()]


if __name__ == "__main__":
    app.run_server(debug=True)
