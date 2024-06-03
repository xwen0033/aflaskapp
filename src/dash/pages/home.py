import os
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
from src.dash.pages import get_placeholder_figure


# Function to analyze files in a folder
def analyze_folder_word_count(folder_path):
    file_list = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.csv')
    ]

    # Create a list to store word counts for each file
    word_counts = {}

    for filename in file_list:
        with open(os.path.join(folder_path, filename), 'r') as file:
            text = file.read()
            words = text.split()
            word_count = len(words)
            word_counts[filename] = word_count
    return word_counts


def plot_word_count(data):
    fig = px.bar(x=list(data.keys()),
                 y=list(data.values()),
                 labels={'x': 'File', 'y': 'Word Count'}, title="Word Count Analysis")
    fig.update_xaxes(type='category')
    return fig


layout = html.Div([
    dcc.Input(id='directory-input', type='text', value='', placeholder='Enter directory path...'),
    html.Button('Submit', id='submit-button'),
    html.Div('', id='selected-directory'),
    dcc.Graph(id='word-count-bar-chart', figure=get_placeholder_figure()),
    dcc.Store(id='click-store', data={'clicks': 0})
])


def register_callbacks(app):
    @app.callback(
        Output('directory-input', "valid"),
        Input('directory-input', 'value')
    )
    def check_path(directory_path):
        if directory_path is None:
            directory_path = ""
        if os.path.isdir(directory_path):
            return True
        return False

    @app.callback(
        Output('selected-directory', 'children'),
        Output('word-count-bar-chart', 'figure'),
        Input('submit-button', 'n_clicks'),
        Input('directory-input', 'value'),
        State('click-store', 'data'),
    )
    def update_output(click, directory_path, data):
        prev_click = data['clicks']
        if click:
            if click != prev_click:
                word_count = analyze_folder_word_count(directory_path)
                update_text = f'Selected Directory: {directory_path}\n Word Count: {word_count}'
                update_fig = plot_word_count(word_count) if word_count != {} else plot_word_count({'None': 0})
                return update_text, update_fig
            else:
                return '', get_placeholder_figure()
        return '', get_placeholder_figure()
