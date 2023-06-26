# Importações do módulo de visualização
from bokeh.palettes import Viridis256
from bokeh.io import save, show, output_file
from bokeh.models import LinearColorMapper, BasicTicker, ColorBar
from bokeh.plotting import figure, curdoc
import read_data

categories = ["Danceability", "Energy", 
              "Valence", "Speechiness", "Acousticness"]

data_spotify = read_data.csv_get_top("visualizacoes/data/spotify_youtube.csv",
                                     "Stream", duplicated_column = "Track")

names_spotify = read_data.csv_get_top_names("visualizacoes/data/spotify_youtube.csv",
                                            "Track", "Stream")


output_file("testando.html")

youtube_plot = figure(title = "Músicas mais ouvidas no Spotify", y_range = names_spotify,
                      height = 400, width = 800)

youtube_plot.hbar(y = "Track", right = "Stream",
                  height = 0.8, source = data_spotify)

show(youtube_plot)
