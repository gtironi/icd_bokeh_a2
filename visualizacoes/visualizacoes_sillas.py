import read_data
from bokeh.io import save, show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange

categories = ["Danceability", "Energy",
              "Valence", "Speechiness",
              "Acousticness"]

