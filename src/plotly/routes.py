from flask import Flask, render_template, request
from src.plotly.pages.word_count import analyze_folder_word_count, plot_word_count
from src.plotly.pages.seasonality import data_preparation, plot_temp
from src.plotly.pages.wave_equation import plot_sine_graph
from src.plotly.pages.weather import get_weather, prepare_weather
from src.plotly.pages.classification import DATA_PATH, OUTPUT_PATH
from src.plotly.utils import read_csv_from_path, save_output

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
            plot_div = plot_word_count(data)
            return render_template("home.html", plot_div=plot_div, folder_path=folder_path)

    return render_template("home.html")


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
            plot_div = plot_temp(winter_x, winter_temp)
            return render_template("seasonality.html", plot_div=plot_div)

    return render_template("seasonality.html")


"""
================================================  
              WAVE EQUATION PAGE
================================================
"""


@app.route("/wave_equation", methods=["GET", "POST"])
def wave_equation():
    plot_div = plot_sine_graph()
    if request.method == "POST":
        a = request.form["user_input"]
        if a != 1:
            plot_div = plot_sine_graph(a)
            return render_template("wave_equation.html", plot_div=plot_div, user_input=a)
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
        return render_template("weather.html", table=table.to_html())
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
