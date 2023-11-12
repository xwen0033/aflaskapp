from flask import Flask, render_template, request
from src.components.word_count import analyze_folder_word_count
from src.components.seasonality import data_preparation
from src.components.weather import get_weather, prepare_weather
from src.components.classification import DATA_PATH, OUTPUT_PATH
import plotly.express as px
from src.utils import read_csv_from_path, save_output
import numpy as np

app = Flask(__name__)

"""
================================================  
              HOME PAGE: Word Counts
================================================
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        folder_path = request.form["folder_path"]
        data = analyze_folder_word_count(folder_path)

        if data:
            fig = px.bar(data, x="File", y="Word Count", title="Word Count Analysis")
            fig.update_xaxes(type='category')
            plot_div = fig.to_html(full_html=False)

            return render_template("index.html", plot_div=plot_div, folder_path=folder_path)

    return render_template("index.html")


"""
================================================  
              SEASONALITY PAGE
================================================
"""


@app.route("/seasonality", methods=["GET", "POST"])
def seasonality():
    if request.method == "POST":
        data_path = request.form["data_path"]
        weather = read_csv_from_path(data_path)

        if not weather.empty:
            winter_x, winter_temp = data_preparation(weather)
            fig = px.line(x=winter_x, y=winter_temp, title="Seasonality Analysis")
            plot_div = fig.to_html(full_html=False)
            return render_template("seasonality.html", plot_div=plot_div)

    return render_template("seasonality.html")


"""
================================================  
              WAVE EQUATION PAGE
================================================
"""


@app.route("/wave_equation", methods=["GET", "POST"])
def wave_equation():
    x = np.linspace(0, 20, 401)
    fig = px.line(x=x, y=np.sin(x), title="Sine Graph")
    plot_div = fig.to_html(full_html=False)
    if request.method == "POST":
        user_a = np.int64(request.form["input-a"])
        if user_a != 1:
            fig = px.line(x=x, y=np.sin(user_a * x), title="Sine Graph")
            plot_div = fig.to_html(full_html=False)
            return render_template("wave_equation.html", plot_div=plot_div)

    return render_template("wave_equation.html", plot_div=plot_div)


"""
================================================  
              WEATHER PAGE
================================================
"""


@app.route("/weather", methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        weather_data = get_weather(lat, lon)
        table = prepare_weather(weather_data)
        return render_template("weather.html", weather_data=weather_data, table=table.to_html())

    return render_template("weather.html")


"""
================================================  
              CLASSIFICATION PAGE
================================================
"""


@app.route("/classification", methods=["GET", "POST"])
def classification():
    data = read_csv_from_path(DATA_PATH)
    data = data.head()
    if request.method == "POST":
        classification = request.form["classification"]
        output = data.to_dict()
        output['category'] = classification
        save_output(output, OUTPUT_PATH)
        saved = 'Successfully saved to output!'
        return render_template("classification.html", table=data.to_html(), saved=saved)

    return render_template("classification.html", table=data.to_html())
