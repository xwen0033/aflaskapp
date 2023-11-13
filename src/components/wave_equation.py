import plotly.express as px
import numpy as np


def plot_sine_graph(a=1):
    a = np.int64(a)
    x = np.linspace(0, 20, 401)
    fig = px.line(x=x, y=np.sin(a * x), title="Sine Graph")
    return fig.to_html(full_html=False)