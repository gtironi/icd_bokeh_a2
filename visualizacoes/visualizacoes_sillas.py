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

################################################################################

# spotify_plot = figure(title = "Músicas mais ouvidas no Spotify", y_range = names_spotify,
#                       height = 300, width = 700)

# spotify_plot.hbar(y = "Track", right = "Stream",
#                   height = 0.8, source = data_spotify)

# show(spotify_plot)

################################################################################

# density_plot = figure(title = f"{initial_category} X Vezes tocadas no Spotify")

# histogram_data = read_data.histogram_count("visualizacoes/data/spotify_youtube.csv",
#                                         initial_category, 10, proportion_column = "Stream")

# density_plot.quad(top = histogram_data[0], bottom = 0,
#                     left = histogram_data[1][:-1],
#                     right = histogram_data[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)

# density_plot.circle(x = initial_category, y = "Stream", source = all_data)


# def update_density_plot(attr, old, new):
#     new_category = filter_category.value
#     density_plot.renderers = []

#     density_plot.title.text = f"{new_category} X Vezes tocadas no Spotify"
#     density_plot.xaxis.axis_label = new_category
    
#     histogram_data = read_data.histogram_count("visualizacoes/data/spotify_youtube.csv",
#                                         new_category, 10, proportion_column = "Stream")
    
#     density_plot.quad(top = histogram_data[0], bottom = 0,
#                     left = histogram_data[1][:-1],
#                     right = histogram_data[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)
    
#     density_plot.circle(x = new_category, y = "Stream", source = all_data)


# filter_category.on_change("value", update_density_plot)

# layout = column(filter_category, density_plot)

# curdoc().add_root(layout)

################################################################################

# dare_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube.csv",
#                                      "Track", "DARE")

# filter_plot = figure(x_range = categories,
#                      title = "Testando a plotagem")

# filter_plot.vbar(x = "Columns", top = "Values", source = dare_data, width = 0.8)

# show(filter_plot)

