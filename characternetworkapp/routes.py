from characternetworkapp import app
import json, plotly
from flask import render_template, request
from wrangling_scripts.wrangle_data import return_figures, return_movies, get_movie_file

@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    movies = []
    if request.method == "GET":
        movies = return_movies()

    return render_template("index.html", movies=movies, ids=[])

@app.route('/', methods=["POST"])
@app.route('/index', methods=["POST"])
def plot_network():
    if request.method == "POST":
        movies = return_movies()
        movie_file = get_movie_file(request.form['movie'])
        figures = return_figures(movie_file, request.form['movie'])
        ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

        # Convert the plotly figures to JSON for javascript in html template
        figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", movies=movies, ids=ids, figuresJSON=figuresJSON)
