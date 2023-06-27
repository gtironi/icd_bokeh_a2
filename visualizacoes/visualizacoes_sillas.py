# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
import read_data

categories = ["Danceability", "Energy", 
              "Valence", "Speechiness", "Acousticness"]

data_spotify = read_data.csv_get_top("visualizacoes/data/spotify_youtube.csv",
                                     "Stream", duplicated_column = "Track")

names_spotify = read_data.csv_get_top_names("visualizacoes/data/spotify_youtube.csv",
                                            "Track", "Stream")

all_data = read_data.csv_to_columndatasouce("visualizacoes/data/spotify_youtube.csv")

output_file("testando.html")

# spotify_plot = figure(title = "Músicas mais ouvidas no Spotify", y_range = names_spotify,
#                       height = 300, width = 700)

# spotify_plot.hbar(y = "Track", right = "Stream",
#                   height = 0.8, source = data_spotify)

# show(spotify_plot)

histogram = read_data.histogram_count("visualizacoes/data/spotify_youtube.csv",
                                      "Danceability", 10, proportion_column = "Stream")

dance_plot = figure()

dance_plot.quad(top = histogram[0], bottom = 0,
                left = histogram[1][:-1],
                right = histogram[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)

dance_plot.circle(x = "Danceability", y = "Stream", source = all_data)


show(dance_plot)
