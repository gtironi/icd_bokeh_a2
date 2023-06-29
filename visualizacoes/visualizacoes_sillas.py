# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Button, TextInput, Div, RangeSlider, BoxAnnotation, PolyAnnotation
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, TapTool
from bokeh.transform import dodge
import read_data



all_data = read_data.csv_to_columndatasource("visualizacoes/data/spotify_youtube_year.csv")

all_music_names = read_data.get_column_observations("visualizacoes/data/spotify_youtube_year.csv",
                                         "Track", sort_column = "Stream")

all_music_names_lower = read_data.get_column_observations("visualizacoes/data/spotify_youtube_year.csv",
                                         "Track", sort_column = "Stream", lowercase = True)


years_data = read_data.get_statistic_by_year("visualizacoes/data/spotify_youtube_year.csv",
                                       "release_date", "popularity")

years = years_data.data["Years"]

firts_music_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                     "Track", all_music_names[0])

first_music_values, firts_music_row = firts_music_data

top_columns = {"Streamed Times": "Stream",
               "Popularity": "popularity"}

categories = ["Danceability", "Energy", "Valence", "Speechiness", "Acousticness"]

top_ten_categories_mean = {"Danceability": 0.6999, "Energy": 0.5804,
                           "Valence": 0.6048, "Speechiness": 0.06073,
                           "Acousticness": 0.342142}
categories_means = []

for column_name in first_music_values.data["Columns"]:
    column_data = column_name
    if column_data in categories:
        column_data = top_ten_categories_mean[column_name]
    
    categories_means.append(column_data)

first_music_values.data["Means"] = categories_means

initial_category = categories[0]

histogram_data = read_data.histogram_data("visualizacoes/data/spotify_youtube_year.csv",
                                        initial_category, proportion_column = "Stream")

filter_category = Select(title = "Categorias", value = initial_category, options = categories)

filter_music = Select(title = "Músicas disponíveis", options = all_music_names,
                       value = all_music_names[0])

filter_top = Select(title = "Opções", options = list(top_columns.keys()),
                    value = "Stream")

# output_file("testando.html")

# Top spotify Plot
################################################################################

years_plot = figure(title = "Years", height = 700, width = 800,
                    x_axis_label = None, y_axis_label = None,
                    x_range = [1993, 2022], y_range = [0, 100])

years_plot.line(x = "Years", y = "Values", source = years_data)

years_plot.circle(x = "Years", y = "Values", source = years_data)

box = BoxAnnotation(left = 2016.5, right = 2021.5, bottom = 60, top = 82,
                    fill_alpha = 0.3, fill_color = 'red')

years_plot.add_layout(box)

# Density Plot
###############################################################################

density_plot = figure(title = f"{initial_category} X Vezes tocadas no Spotify")
density_plot.xaxis.axis_label = initial_category

density_plot.xaxis[0].formatter = NumeralTickFormatter(format = "#0%")

density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                  fill_color = 'skyblue', fill_alpha = 0.7, source = histogram_data)

density_plot.circle(x = initial_category, y = "Stream", source = all_data)

density_plot.circle(x = initial_category, y = "Stream", source = firts_music_row,
                    size = 20, fill_color = "red")

# Track Plot
################################################################################

filter_plot = figure(x_range = categories, title = f"{all_music_names[0]} Stats")
filter_plot.xaxis.axis_label = all_music_names[0]

filter_plot.yaxis[0].formatter = NumeralTickFormatter(format = "#0%")

filter_plot.vbar(x = dodge("Columns", -0.15, range = filter_plot.x_range),
                 top = "Values", source = first_music_values, width = 0.25)

filter_plot.vbar(x = dodge("Columns", 0.15, range = filter_plot.x_range),
                 top = "Means", source = first_music_values, width = 0.25)

spotify_player_html = f"""
<iframe src="https://open.spotify.com/embed?uri={firts_music_row.data["Uri"][0]}"
        width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
"""

spotify_player = Div(text=spotify_player_html)

# Year Plot Filter
###############################################################################

years_selection = RangeSlider(title = "Selecione o intervalo de anos desejados",
                            start = min(years), end = max(years),
                            value = (1993, max(years)), step = 1,
                            width = 400)

def update_years(attr, old, new):
    start, end = years_selection.value

    years_plot.x_range.start = start
    years_plot.x_range.end = end

years_selection.on_change("value", update_years)

column_years = column(years_selection, years_plot)

# Density Plot Filter
###############################################################################

def update_density_plot(attr, old, new):
    new_category = filter_category.value
    density_plot.renderers = []

    density_plot.title.text = f"{new_category} X Vezes tocadas no Spotify"
    density_plot.xaxis.axis_label = new_category
        
    histogram_data = read_data.histogram_data("visualizacoes/data/spotify_youtube_year.csv",
                                        new_category, proportion_column = "Stream")
        
    density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                      fill_color = 'skyblue', fill_alpha = 0.7, source = histogram_data)
        
    density_plot.circle(x = new_category, y = "Stream", source = all_data)

    update_music_circle(filter_plot.xaxis.axis_label, new_category)


def update_music_circle(music_name, category_type):
    if len(density_plot.renderers) > 2:
        del density_plot.renderers[2]

    filter_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                            "Track", music_name, lowercase = True)
    
    density_plot.circle(x = category_type, y = "Stream", source = filter_data[1],
                        size = 20, fill_color = "red")


filter_category.on_change("value", update_density_plot)

column_density_plot = column(filter_category, density_plot)

# Track Plot Filter
################################################################################

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
    
    new_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                                    "Track", new_music, lowercase = True)
    values, row = new_data
    music_name = row.data["Track"][0]
    music_uri = row.data["Uri"][0]

    filter_plot.renderers = []
        
    filter_music.value = music_name

    filter_plot.title.text = f"{music_name} Stats"
    filter_plot.xaxis.axis_label = music_name
    filter_plot.vbar(x = "Columns", top = "Values", source = values, width = 0.8)

    update_spotify_player(music_uri)
    update_music_circle(music_name, density_plot.xaxis.axis_label)


filter_music.on_change("value", update_music_selected)

layout = row(column(search_input, search_button, filter_music, spotify_player),
             filter_plot, column_density_plot, column_years)

curdoc().add_root(layout)
