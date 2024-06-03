from dash import html, dcc
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output, State

def plot_sine_graph(a=1):
    a = np.int64(a)
    x = np.linspace(0, 20, 401)
    fig = px.line(x=x, y=np.sin(a * x), title="Sine Graph")
    return fig


layout = html.Div([
    dcc.Input(id='a-input', type='number', placeholder='1'),
    html.Button('Update Graph', id='update-a'),
    dcc.Graph(id='sine-graph', figure=plot_sine_graph()),
    dcc.Store(id='click-store-3', data={'clicks': 0})
])


def register_callbacks(app):
    @app.callback(
        Output('click-store-3', 'data'),
        Input('update-a', 'n_clicks'),
        State('click-store-3', 'data')
    )
    def update_click_count(click, data):
        data['clicks'] = click
        return data


    @app.callback(
        Output('sine-graph', 'figure'),
        Input('update-a', 'n_clicks'),
        Input('a-input', 'value'),
        State('click-store-3', 'data'),
    )
    def update_output(click, a, data):
        prev_click = data['clicks']
        if click:
            if click != prev_click:
                update_fig = plot_sine_graph(a)
                return update_fig
            else:
                return plot_sine_graph()
        return plot_sine_graph()