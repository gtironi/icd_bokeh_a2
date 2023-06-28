# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Button, TextInput, Div
import read_data


data_spotify = read_data.csv_get_top("visualizacoes/data/spotify_youtube_year.csv",
                                     "Stream", duplicated_column = "Track")

names_spotify = read_data.csv_get_top_names("visualizacoes/data/spotify_youtube_year.csv",
                                            "Track", "Stream")

all_data = read_data.csv_to_columndatasource("visualizacoes/data/spotify_youtube_year.csv")

all_music_names = read_data.get_column_observations("visualizacoes/data/spotify_youtube_year.csv",
                                         "Track", sort_column = "Stream")

all_music_names_lower = read_data.get_column_observations("visualizacoes/data/spotify_youtube_year.csv",
                                         "Track", sort_column = "Stream", lowercase = True)

categories = ["Danceability", "Energy", "Valence", "Speechiness", "Acousticness"]

initial_category = categories[0]

histogram_data = read_data.histogram_count("visualizacoes/data/spotify_youtube_year.csv",
                                        initial_category, 10, proportion_column = "Stream")

firts_music_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                     "Track", all_music_names[0])

firt_music_values, firts_music_row = firts_music_data

filter_category = Select(title = "Categorias", value = initial_category, options = categories)


output_file("testando.html")

# Top Tracks Plot
################################################################################

top_tracks_plot = figure(title = "Músicas mais ouvidas no Spotify", y_range = names_spotify,
                      height = 300, width = 700)

top_tracks_plot.hbar(y = "Track", right = "Stream",
                  height = 0.8, source = data_spotify)

# Density Plot
###############################################################################

density_plot = figure(title = f"{initial_category} X Vezes tocadas no Spotify")

density_plot.quad(top = histogram_data[0], bottom = 0,
                    left = histogram_data[1][:-1],
                    right = histogram_data[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)

density_plot.circle(x = initial_category, y = "Stream", source = all_data)

density_plot.circle(x = initial_category, y = "Stream", source = firts_music_row,
                    size = 20, fill_color = "red")

# Track Plot
################################################################################

filter_plot = figure(x_range = categories, title = f"{all_music_names[0]} Stats")

filter_plot.vbar(x = "Columns", top = "Values", source = firt_music_values, width = 0.8)

spotify_player_html = f"""
<iframe src="https://open.spotify.com/embed?uri={firts_music_row.data["Uri"][0]}"
        width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
"""

spotify_player = Div(text=spotify_player_html)

# Density Plot Filter
###############################################################################

def update_density_plot(attr, old, new):
    new_category = filter_category.value
    density_plot.renderers = []

    density_plot.title.text = f"{new_category} X Vezes tocadas no Spotify"
    density_plot.xaxis.axis_label = new_category
    
    histogram_data = read_data.histogram_count("visualizacoes/data/spotify_youtube_year.csv",
                                        new_category, 10, proportion_column = "Stream")
    
    density_plot.quad(top = histogram_data[0], bottom = 0,
                    left = histogram_data[1][:-1],
                    right = histogram_data[1][1:], fill_color = 'skyblue', fill_alpha = 0.7)
    
    density_plot.circle(x = new_category, y = "Stream", source = all_data)


filter_category.on_change("value", update_density_plot)

column_density_plot = column(filter_category, density_plot)

# Track Plot Filter
################################################################################

filter_music = Select(title = "Músicas disponíveis", options = all_music_names,
                       value = all_music_names[0])


def update_spotify_player(spotify_uri):
    spotify_player_html = f"""
    <iframe src="https://open.spotify.com/embed?uri={spotify_uri}"
            width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """
    spotify_player.text = spotify_player_html

def make_search():
    search_term = search_input.value.lower()

    if search_term in all_music_names_lower:
        filter_music.value = search_term
        update_music_selected(None, None, None)

search_input = TextInput(title="Busque uma música", value="")

search_button = Button(label="Buscar", button_type = "success")
search_button.on_click(make_search)

def update_music_selected(attr, old, new):
    new_music = filter_music.value
    filter_plot.renderers = []

    new_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                                   "Track", new_music, lowercase = True)
    values, row = new_data
    music_name = row.data["Track"][0]
    music_uri = row.data["Uri"][0]
    
    filter_music.value = music_name

    filter_plot.title.text = f"{music_name} Stats"
    filter_plot.vbar(x = "Columns", top = "Values", source = values, width = 0.8)
    update_spotify_player(music_uri)

filter_music.on_change("value", update_music_selected)

layout = row(column(search_input, search_button, filter_music, spotify_player),
             filter_plot, top_tracks_plot, column_density_plot)

curdoc().add_root(layout)
