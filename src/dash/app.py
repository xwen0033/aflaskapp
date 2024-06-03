""" initializes the Dash app, sets up the layout, and runs the server"""
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from src.dash.components.footer import footer
from src.dash.components.navbar import navbar
from pages import home, wave_equation, weather, seasonality, classification
from utils import read_csv_from_path, save_output

app = Dash(__name__)
app.config["suppress_callback_exceptions"] = True
# Define page layouts
# Set the initial layout dynamically within the callback
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", fluid=True),  # Placeholder for page content
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
        return [wave_equation.layout]
    elif pathname == "/seasonality":
        return [seasonality.layout]
    elif pathname == "/weather":
        return [weather.get_layout()]
    elif pathname == "/classification":
        return [classification.get_layout()]
    else:
        return [home.layout]


def create_callback(button_id, input_id, click_store_id):
    @app.callback(
        Output(button_id, "style"),
        Input(input_id, 'valid')
    )
    def check_valid(valid_path):
        style = {"margin-bottom": "1.5rem",
                 "font-weight": "700", "background": "red"}
        if valid_path:
            style = {"margin-bottom": "1.5rem",
                     "font-weight": "700", "background": "green"}
        return style

    @app.callback(
        Output(button_id, "disabled"),
        Input(button_id, "style")
    )
    def update_button(btn_style):
        if btn_style["background"] == "green":
            return False
        else:
            return True

    @app.callback(
        Output(click_store_id, 'data'),
        Input(button_id, 'n_clicks'),
        State(click_store_id, 'data')
    )
    def update_click_count(click, data):
        data['clicks'] = click
        return data



create_callback('submit-button', 'directory-input', 'click-store')
create_callback('submit-file', 'file-input', 'click-store-2')
home.register_callbacks(app)
seasonality.register_callbacks(app)
wave_equation.register_callbacks(app)



if __name__ == "__main__":
    app.run_server(debug=True)
