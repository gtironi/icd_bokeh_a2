# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import Select
import read_data

# data_spotify = read_data.csv_get_top("visualizacoes/data/spotify_youtube.csv",
#                                      "Stream", duplicated_column = "Track")

# names_spotify = read_data.csv_get_top_names("visualizacoes/data/spotify_youtube.csv",
#                                             "Track", "Stream")

all_data = read_data.csv_to_columndatasource("visualizacoes/data/spotify_youtube.csv")


categories = ["Danceability", "Energy", 
              "Valence", "Speechiness", "Acousticness"]

initial_category = categories[0]

filter_category = Select(title = "Categorias", value = initial_category, options = categories)

output_file("testando.html")

# spotify_plot = figure(title = "Músicas mais ouvidas no Spotify", y_range = names_spotify,
#                       height = 300, width = 700)

# spotify_plot.hbar(y = "Track", right = "Stream",
#                   height = 0.8, source = data_spotify)

# show(spotify_plot)

density_plot = figure(title = f"{initial_category} X Vezes tocadas no Spotify")

histogram = read_data.histogram_count("visualizacoes/data/spotify_youtube.csv",
                                        initial_category, 10, proportion_column = "Stream")

density_plot.quad(top = histogram[0], bottom = 0,
                    left = histogram[1][:-1],
                    right = histogram[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)

density_plot.circle(x = initial_category, y = "Stream", source = all_data)


def update_density_plot(attr, old, new):
    curdoc().clear()
    category = filter_category.value

    density_plot = figure(title = f"{category} X Vezes tocadas no Spotify")
    
    histogram = read_data.histogram_count("visualizacoes/data/spotify_youtube.csv",
                                        category, 10, proportion_column = "Stream")

    density_plot.quad(top = histogram[0], bottom = 0,
                    left = histogram[1][:-1],
                    right = histogram[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)

    density_plot.circle(x = category, y = "Stream", source = all_data)
    
    layout = column(filter_category, density_plot)

    curdoc().add_root(layout)

filter_category.on_change("value", update_density_plot)

layout = column(filter_category, density_plot)

curdoc().add_root(layout)

