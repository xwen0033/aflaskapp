import os

from dash import html, dcc
from src.dash.pages import get_placeholder_figure
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

# TODO: Fix the data preparation
def data_preparation(weather: pd.DataFrame):
    weather.index = pd.to_datetime(weather.index, dayfirst=True)
    range = weather.index[
        (weather.index < pd.to_datetime('2018-09-01'))
        & (weather.index >= pd.to_datetime('2018-06-01'))
        ]

    winter_max = weather.loc[range, :].Max.tolist()
    winter_min = weather.loc[range, :].Min.tolist()
    winter_x = weather.loc[range, :].index.tolist()
    winter_temp = winter_max + winter_min[::-1]
    winter_x = winter_x + winter_x[::-1]
    return winter_x, winter_temp


def plot_temp(winter_x, winter_temp):
    fig = px.line(x=winter_x, y=winter_temp, title="Seasonality Analysis")
    return fig.to_html(full_html=False)


layout = html.Div([
        dcc.Input(id='file-input', type='text', value='', placeholder='Enter csv file path...'),
        html.Button('Submit', id='submit-file'),
        dcc.Graph(id='temperature-graph', figure=get_placeholder_figure()),
        dcc.Store(id='click-store-2', data={'clicks': 0})
    ])


def register_callbacks(app):

    @app.callback(
        Output('file-input', "valid"),
        Input('file-input', 'value')
    )
    def check_file(file_path):
        if file_path is None:
            file_path = ""
        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            return True
        return False

    @app.callback(
        Output('temperature-graph', 'figure'),
        Input('submit-file', 'n_clicks'),
        Input('file-input', 'value'),
        State('click-store-2', 'data'),
    )
    def update_output(click, file_path, data):
        prev_click = data['clicks']
        if click:
            if click != prev_click:
                x, temp = data_preparation(file_path)
                update_fig = plot_temp(x, temp)
                return update_fig
            else:
                return get_placeholder_figure()
        return get_placeholder_figure()