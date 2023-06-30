# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Button, TextInput, Div, RangeTool, BoxAnnotation
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool, Label, TapTool
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

filter_category = Select(title = "Tente alterar a categoria selecionada", value = initial_category, options = categories,
                         height = 35, width = 640,)

filter_music = Select(title = "Músicas disponíveis:", options = all_music_names,
                       value = all_music_names[0], height = 35, width = 640,)

# output_file("testando.html")

# Mean popularity by Year Plot
################################################################################

years_plot = figure(title = "Crescimento da Popularidade média das músicas por Ano",
                    height = 350, width = 640, tools = "xpan", toolbar_location = None,
                    x_range = [2001, 2021], y_range = [0, 100],
                    x_axis_label = "Anos", y_axis_label = "Popularidade Média",)

years_plot.background_fill_color="WhiteSmoke"
years_plot.xgrid.grid_line_color = None
years_plot.yaxis.ticker = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

years_plot.line(x = "Years", y = "Values", source = years_data,
                line_color = "SpringGreen")

years_plot.circle(x = "Years", y = "Values", size = 7, source = years_data,
                  fill_color = "MediumSeaGreen")

# Years plot Annotations

best_popularity_years_annotation = BoxAnnotation(left = 2016.5, right = 2021.5, bottom = 60, top = 85,
                    fill_alpha = 0.3, fill_color = 'BlueViolet')

years_plot.add_layout(best_popularity_years_annotation)

best_popularity_years_label = Label(x = 2015, y = 80,
                    text = "Popularidade média\nvem aumentando\ndesde 2017.",
                    text_align = "center", text_font_size = "12px")

years_plot.add_layout(best_popularity_years_label)

# Years plot Slider

select_years = figure(title = "Arraste para selecionar os anos desejados da observação",
                    height = 130, width = 640, y_range = years_plot.y_range,
                    y_axis_type = None, tools = "", toolbar_location = None)

select_years.background_fill_color="WhiteSmoke"
select_years.xgrid.grid_line_color = None

select_years_tool = RangeTool(x_range = years_plot.x_range)
select_years_tool.overlay.fill_color = "MediumAquamarine"
select_years_tool.overlay.fill_alpha = 0.2

select_years.line(x = "Years", y = "Values", source = years_data,
                line_color = "SpringGreen")
select_years.circle(x = "Years", y = "Values", size = 2, source = years_data,
                  fill_color = "MediumSeaGreen")
select_years.add_layout(best_popularity_years_annotation)
select_years.ygrid.grid_line_color = None
select_years.add_tools(select_years_tool)

column_years = column(years_plot, select_years)

# Density Plot
###############################################################################

density_plot = figure(height=480, width=640, title = f"{initial_category} X Vezes tocadas no Spotify (Em bilhões)",
                      x_range = [0, 1], y_range = [0, 3500000000])
density_plot.xaxis.axis_label = initial_category
density_plot.xaxis.ticker = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
density_plot.yaxis.axis_label = "Número de vezes escutadas no Spotify"
density_plot.yaxis.ticker = [0, 500000000, 1000000000, 1500000000, 2000000000, 2500000000, 3000000000, 3500000000]
density_plot.background_fill_color="WhiteSmoke"
density_plot.xgrid.grid_line_color = None
density_plot.ygrid.grid_line_color = None

density_plot.xaxis.formatter = NumeralTickFormatter(format = "#0%")
density_plot.yaxis.formatter = NumeralTickFormatter(format = "0.#a")


density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                  fill_color = 'MediumAquamarine', fill_alpha = 0.7, source = histogram_data,
                  line_color = "#535353")

density_plot.circle(x = initial_category, y = "Stream", size = 6, source = all_data,
                    fill_color = "#1DB954", line_color = "DarkGreen",
                    fill_alpha = 0.7)

density_plot.star(x = initial_category, y = "Stream", source = firts_music_row,
                    size = 18, fill_color = "DarkViolet")

# Track Status Plot
################################################################################

filter_plot = figure(height=480, width=640, x_range = categories, title = f"Níveis de {all_music_names[0]}",
                     y_range = [0, 1.15])

filter_plot.xaxis.axis_label = None
filter_plot.background_fill_color = "WhiteSmoke"
filter_plot.xgrid.grid_line_color = None
filter_plot.yaxis.ticker = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

filter_plot.yaxis[0].formatter = NumeralTickFormatter(format = "#0%")

filter_plot.vbar(x = dodge("Columns", 0.22, range = filter_plot.x_range),
                 top = "Means", source = first_music_values, width = 0.41,
                 fill_color = "DarkViolet", legend_label = "Médias das 10 Músicas mais escutadas no Spotify",
                 line_color = "#535353")


filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                 top = "Values", source = first_music_values, width = 0.4,
                 fill_color = "#1ed760", legend_label = all_music_names[0],
                 line_color = "#535353")

filter_plot.legend.background_fill_alpha = 0
filter_plot.legend.border_line_alpha = 0

spotify_player_html = f"""
<iframe src="https://open.spotify.com/embed?uri={firts_music_row.data["Uri"][0]}"
        width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
"""

spotify_player = Div(text=spotify_player_html)


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
                      fill_color = 'MediumAquamarine', fill_alpha = 0.7, source = histogram_data,
                      line_color = "#535353")
        
    density_plot.circle(x = new_category, y = "Stream", size = 6, source = all_data,
                        fill_color = "#1DB954", line_color = "DarkGreen",
                        fill_alpha = 0.7)

    update_music_star(filter_plot.title.text[10:], new_category)


def update_music_star(music_name, category_type):
    if len(density_plot.renderers) > 2:
        del density_plot.renderers[2]

    filter_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                            "Track", music_name, lowercase = True)
    
    density_plot.star(x = category_type, y = "Stream", source = filter_data[1],
                        size = 20, fill_color = "DarkViolet")


filter_category.on_change("value", update_density_plot)


# Track Plot Filter
################################################################################

def update_spotify_player(spotify_uri):
    spotify_player_html = f"""
    <iframe src="https://open.spotify.com/embed?uri={spotify_uri}"
            width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """
    spotify_player.text = spotify_player_html

def make_search():
    search_term = search_input.value.lower()

    if search_term in all_music_names_lower:
        filter_music.value = search_term
        update_music_selected(None, None, None)


search_input = TextInput(title = "Insira uma música e da um Play (Tente inserir como o nome do Spotify):", value = "",
                        width = 500)

search_button = Button(label="Play", button_type = "success", height = 32, width = 140)
search_button.on_click(make_search)

def update_music_selected(attr, old, new):
    new_music = filter_music.value
    
    new_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                                    "Track", new_music, lowercase = True)
    values, row = new_data
    music_name = row.data["Track"][0]
    music_uri = row.data["Uri"][0]

    del filter_plot.renderers[1]
    del filter_plot.legend.items[1]
    
    filter_music.value = music_name

    filter_plot.title.text = f"Níveis de {music_name}"
    filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                     top = "Values", source = values, width = 0.41,
                     fill_color = "#1ed760", legend_label = music_name,
                     line_color = "#535353")

    update_spotify_player(music_uri)
    update_music_star(music_name, density_plot.xaxis.axis_label)


filter_music.on_change("value", update_music_selected)

music_selector = column(row(search_input, column(search_button, align = "end")),
                        row(filter_music), row(Div(text = "<br>")),
                        row(spotify_player),
                        row(Div(text = "<br><br><br><br>")),
                        row(filter_category))

layout = column(row(music_selector, filter_plot),
                row(density_plot, column_years))

curdoc().add_root(layout)

