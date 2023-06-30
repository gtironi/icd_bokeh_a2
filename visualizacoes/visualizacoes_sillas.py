# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Button, TextInput, Div, RangeTool, BoxAnnotation
from bokeh.models import NumeralTickFormatter, HoverTool, Label
from bokeh.transform import dodge
import read_data
import temporary

# output_file("testando.html")

# Leitura de dados para a primeira plotagem
################################################################################

# Primeiro carregaremos todos os nomes de músicas na base de dados, e suas versões com caixa baixa (ordenando por vezes escutadas).
all_music_names = read_data.get_column_observations("visualizacoes/data/spotify_youtube_year.csv",
                                         "Track", sort_column = "Stream")
all_music_names_lower = read_data.get_column_observations("visualizacoes/data/spotify_youtube_year.csv",
                                 "Track", sort_column = "Stream", lowercase = True)

# Agora carregaremos os dados da música mais escutada.
firts_music_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                     "Track", all_music_names[0])

# E separaremos eles em seus valores brutos e a linha obtida.
first_music_values, firts_music_row = firts_music_data

# Agora definiremos as categorias que serão comparadas na primeira plotagem.
categories = ["Danceability", "Energy", "Valence", "Speechiness", "Acousticness"]

# Após obter as médias das 10 primeiras músicas, iremos adicioná-las aos nossos dados.
top_ten_categories_mean = {"Danceability": 0.6999, "Energy": 0.5804,
                           "Valence": 0.6048, "Speechiness": 0.06073,
                           "Acousticness": 0.342142}
categories_means = []

# Se a coluna for uma categoria, adiciona sua média, se não for, adiciona apenas o seu nome
for column_name in first_music_values.data["Columns"]:
    column_data = column_name
    if column_data in categories:
        column_data = top_ten_categories_mean[column_name]
    
    categories_means.append(column_data)

# Adicionaremos uma nova coluna das médias aos dados.
first_music_values.data["Means"] = categories_means


# Track Status Plot
################################################################################

# Deste modo criaremos a primeira plotagem, que irá comparar os níveis por categoria
# da música mais escutada com a média das músicas mais escutadas.
filter_plot = figure(height=480, width=640, title = f"Níveis de {all_music_names[0]}",
                    tools = "xpan", toolbar_location = None,
                    x_range = categories, y_range = [0, 1.15])

# Removeremos alguns parâmetros para fins estéticos.
filter_plot.xaxis.axis_label = None
filter_plot.xgrid.grid_line_color = None
# Adicionaremos os intervalos do eixo Y.
filter_plot.yaxis.ticker = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

# Iremos carregar o tema pré definido de rótulos e cor de fundo.
filter_plot = temporary.figure_text_generator_sillas(filter_plot)

# Alteraremos o formato do eixo Y para exibir porcentagem, como todas as categorias
# vão de 0 à 1, é possível computar seus valores como porcentagens.
filter_plot.yaxis[0].formatter = NumeralTickFormatter(format = "#0%")

# Adicionaremos as colunas das médias do top 10.
médias = filter_plot.vbar(x = dodge("Columns", 0.22, range = filter_plot.x_range),
                 top = "Means", source = first_music_values, width = 0.41,
                 fill_color = "DarkViolet", legend_label = "Médias das 10 Músicas mais escutadas no Spotify",
                 line_color = "#535353")
# Adicionaremos as colunas da música selecionada (a primeira mais escutada).
selected_music = filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                 top = "Values", source = first_music_values, width = 0.4,
                 fill_color = "#1ed760", legend_label = all_music_names[0],
                 line_color = "#535353")

# Removeremos parâmetros desnecessários da legenda para fins estéticos.
filter_plot.legend.background_fill_alpha = 0
filter_plot.legend.border_line_alpha = 0

# Criaremos um hover para as colunas das médias e para as colunas da música selecionada
# e os adicionaremos ao gráfico.
hover_medias = HoverTool(renderers = [médias], tooltips = [("Valor", "@Means")])

hover_musica = HoverTool(renderers = [selected_music], tooltips = [("Valor", "@Values")])

filter_plot.add_tools(hover_medias, hover_musica)

# Criaremos um player do spotify simples com a música selecionada.
spotify_player_html = f"""
<iframe src="https://open.spotify.com/embed?uri={firts_music_row.data["Uri"][0]}"
        width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
"""

spotify_player = Div(text=spotify_player_html)

# Track Plot Filter
################################################################################

# Criaremos um filtro para poder poder escolher entre todas as músicas disponíveis.
filter_music = Select(title = "Músicas disponíveis:", options = all_music_names,
                       value = all_music_names[0], height = 35, width = 640,)

# Adicionaremos uma função que atualiza a música do player dependendo da música que
# for selecionada.
def update_spotify_player(spotify_uri):
    spotify_player_html = f"""
    <iframe src="https://open.spotify.com/embed?uri={spotify_uri}"
            width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """
    spotify_player.text = spotify_player_html

# Adicionaremos a função que atualiza a música selecionada.
def update_music_selected(attr, old, new):
    new_music = filter_music.value
    # Busca os dados da nova música
    new_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                                    "Track", new_music, lowercase = True)
    # Atribui os dados à novas variáveis.
    values, row = new_data
    music_name = row.data["Track"][0]
    music_uri = row.data["Uri"][0]
    # Deleta as partes do gráfico da última música.
    del filter_plot.renderers[1]
    del filter_plot.legend.items[1]
    
    filter_music.value = music_name
    # Atualiza o título do gráfico.
    filter_plot.title.text = f"Níveis de {music_name}"
    # Atualiza as colunas da música selecionada.
    selected_music = filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                     top = "Values", source = values, width = 0.41,
                     fill_color = "#1ed760", legend_label = music_name,
                     line_color = "#535353")
    # Recria o hover toll.
    new_hover = HoverTool(renderers = [selected_music],
                  tooltips = [("Valor", "@Values")])
    filter_plot.add_tools(new_hover)

    # Atualiza o player do spotify com a nova música.
    update_spotify_player(music_uri)
    # E indica a música no gráfico de densidade.
    update_music_star(music_name, density_plot.xaxis.axis_label)

# Adicionaremos a iteratividade da função e da seleção de músicas.
filter_music.on_change("value", update_music_selected)

# Adicionaremos a função que possibilita fazer buscas por músicas pelos nomes.
def make_search():
    search_term = search_input.value.lower()
    # Se o nome da música for válido, atualiza a música selecionada.
    if search_term in all_music_names_lower:
        filter_music.value = search_term
        update_music_selected(None, None, None)

# Adicionaremos a entrada para a pesquisa da música.
search_input = TextInput(title = "Insira uma música e da um Play (Tente inserir como o nome do Spotify):", value = "",
                        width = 500)
# Adicionaremos o botão de pesquisa da música.
search_button = Button(label="Play", button_type = "success", height = 32, width = 140)
# Ao clicar ele realizará a pesquisa.
search_button.on_click(make_search)

# Leitura de dados para a segunda plotagem
###############################################################################

# Leremos todos os dados
all_data = read_data.csv_to_columndatasource("visualizacoes/data/spotify_youtube_year.csv")

# Definiremos a categoria inicial como uma das categorias da primeira plotagem.
initial_category = categories[0]
# Obteremos os dados de histograma para a plotagem.
histogram_data = read_data.histogram_data("visualizacoes/data/spotify_youtube_year.csv",
                                        initial_category, proportion_column = "Stream")

# Density Plot
###############################################################################

# Criaremos o gráfico de densidade que terá como base a exibição do quanto as
# categegorias estão presentes em uma música e quantas vezes ela foi ouvida, para atestar
# a correlação entre as categorias e a quantidade de vezes que elas foram ouvidas.
density_plot = figure(height=480, width=640, title = f"{initial_category} X Vezes tocadas no Spotify (Em bilhões)",
                      tools = "xpan", toolbar_location = None,
                      x_range = [0, 1], y_range = [0, 3500000000])

# Formataremos o eixo X.
density_plot.xaxis.axis_label = initial_category
density_plot.xaxis.ticker = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# Agora o eixo Y.
density_plot.yaxis.axis_label = "Número de vezes escutadas no Spotify"
density_plot.yaxis.ticker = [0, 500000000, 1000000000, 1500000000, 2000000000, 2500000000, 3000000000, 3500000000]
# Removeremos as linhas de grid.
density_plot.xgrid.grid_line_color = None
density_plot.ygrid.grid_line_color = None

# Utilizaremos o tema pré definido.
density_plot = temporary.figure_text_generator_sillas(density_plot)

# Alteraremos o formato dos eixos, o eixo x novamente irá de 0 à 1 pois é uma das categorias,
# entretanto o eixo Y chega à escala de bilhões.
density_plot.xaxis.formatter = NumeralTickFormatter(format = "#0%")
density_plot.yaxis.formatter = NumeralTickFormatter(format = "0.#a")

# Geraremos o histograma da distribuição à partir dos dados, o objetivo é exibir o
# agrupamento dos dados.
density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                  fill_color = 'MediumAquamarine', fill_alpha = 0.7, source = histogram_data,
                  line_color = "#535353")
# Agora geraremos todas as músicas em um scatter plot onde o eixo X é a categoria
# e o Y é a quantidade de vezes ouvidas.
musics = density_plot.circle(x = initial_category, y = "Stream", size = 6, source = all_data,
                    fill_color = "#1DB954", line_color = "DarkGreen",
                    fill_alpha = 0.7)
# Daremos destaque a música selecionada do outro gráfico.
density_plot.star(x = initial_category, y = "Stream", source = firts_music_row,
                    size = 18, fill_color = "DarkViolet")

# Adicionaremos um hover com os dados das músicas ao gráfico.
musics_hover = HoverTool(renderers = [musics],
                  tooltips = [("Música", "@Track"), ("Artista", "@Artist")])

density_plot.add_tools(musics_hover)

# Density Plot Filter
###############################################################################

# Criaremos a seleção das categorias:
filter_category = Select(title = "Tente alterar a categoria selecionada", value = initial_category, options = categories,
                         height = 35, width = 640,)

# Função que atualiza as categorias:
def update_density_plot(attr, old, new):
    # Recebe a nova categoria e limpa o gráfico.
    new_category = filter_category.value
    density_plot.renderers = []
    # Atualiza os rótulos do gráfico para a nova categoria.
    density_plot.title.text = f"{new_category} X Vezes tocadas no Spotify"
    density_plot.xaxis.axis_label = new_category
    # Gera o novo histograma.
    histogram_data = read_data.histogram_data("visualizacoes/data/spotify_youtube_year.csv",
                                        new_category, proportion_column = "Stream")
    # E então plota o histograma com a nova categoria.
    density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                      fill_color = 'MediumAquamarine', fill_alpha = 0.7, source = histogram_data,
                      line_color = "#535353")
    # Gera o gráfico das músicas.
    musics = density_plot.circle(x = new_category, y = "Stream", size = 6, source = all_data,
                        fill_color = "#1DB954", line_color = "DarkGreen",
                        fill_alpha = 0.7)
    # Adiciona novamente o hover das músicas ao gráfico
    musics_hover = HoverTool(renderers = [musics],
                    tooltips = [("Música", "@Track"), ("Artista", "@Artist")])
    density_plot.add_tools(musics_hover)
    # E então atualiza a posição música selecionada com a nova categoria.
    update_music_star(filter_plot.title.text[10:], new_category)

# Agora adicionaremos a iteratividade entre a seleção de categorias e sua função de atualização.
filter_category.on_change("value", update_density_plot)

# Função que atualiza a posição da música selecionada a partir do seu nome e nova categoria:
def update_music_star(music_name, category_type):
    # Se já existir uma, ela será deletada.
    if len(density_plot.renderers) > 2:
        del density_plot.renderers[2]

    # Obtém os novos dados da música selecionada
    filter_data = read_data.csv_filter_by_name_to_cds("visualizacoes/data/spotify_youtube_year.csv",
                                            "Track", music_name, lowercase = True)
    # Plota novamente a música selecionada
    density_plot.star(x = category_type, y = "Stream", source = filter_data[1],
                        size = 20, fill_color = "DarkViolet")

# Leitura dos dados para a terceira plotagem
################################################################################

# Obteremos os dados dos anos e da popularidade média por ano.
years_data = read_data.get_statistic_by_year("visualizacoes/data/spotify_youtube_year.csv",
                                       "release_date", "popularity")
# Obteremos os anos.
years = years_data.data["Years"]

# Mean popularity by Year Plot
################################################################################

# Geraremos a figura dos anos.
years_plot = figure(title = "Crescimento da Popularidade média das músicas por Ano",
                    height = 350, width = 640, tools = "xpan", toolbar_location = None,
                    x_range = [2001, 2021], y_range = [0, 100],
                    x_axis_label = "Anos", y_axis_label = "Popularidade Média",)
# Adicionaremos o tema pré definido à figura.
years_plot = temporary.figure_text_generator_sillas(years_plot)
# Removeremos o grid do eixo X para uma análise temporal.
years_plot.xgrid.grid_line_color = None
# Adicionaremos os intervalos do eixo Y.
years_plot.yaxis.ticker = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Geraremos o gráfico de linhas temporais
line_years = years_plot.line(x = "Years", y = "Values", source = years_data,
                line_color = "SpringGreen")
# Adicionaremos círculos no pontos dos anos.
circles_years = years_plot.circle(x = "Years", y = "Values", size = 7, source = years_data,
                  fill_color = "MediumSeaGreen")

# Criaremos um hover e o adicionaremos ao gráfico para exibir o ano e a popularidade média do ano.
circle_years_hover = HoverTool(renderers = [circles_years, line_years],
                  tooltips = [("Popularidade Média", "@Values"), ("Anos", "@Years")])

years_plot.add_tools(circle_years_hover)

### Year plot Annotations

# Iremos adicionar uma caixa de anotações para destacar dados de aumento da popularidade média.
best_popularity_years_annotation = BoxAnnotation(left = 2016.5, right = 2021.5, bottom = 60, top = 85,
                    fill_alpha = 0.3, fill_color = 'BlueViolet')

years_plot.add_layout(best_popularity_years_annotation)

# Iremos adicionar um texto simples indicando o motivo da caixa de anotações.
best_popularity_years_label = Label(x = 2015, y = 80,
                    text = "Popularidade média\nvem aumentando\ndesde 2017.",
                    text_align = "center", text_font_size = "12px")

years_plot.add_layout(best_popularity_years_label)

### Year plot Slider

# Iremos criar uma figura para poder percorrer pelos anos de maneira dinâmica.
select_years = figure(title = "Arraste para selecionar os anos desejados da observação",
                    height = 130, width = 640, y_range = years_plot.y_range,
                    y_axis_type = None, tools = "", toolbar_location = None)

# Iremos passar alguns parâmetros estéticos.
select_years.background_fill_color="WhiteSmoke"
select_years.xgrid.grid_line_color = None
select_years.ygrid.grid_line_color = None

# E por fim, alteraremos o seu título.
select_years.title.text_color = "Black"
select_years.title.text_font = "Arial Black"
select_years.title.align = "center"

# Iremos fazer a nova figura semelhante à original.
select_years.line(x = "Years", y = "Values", source = years_data,
                line_color = "SpringGreen")
select_years.circle(x = "Years", y = "Values", size = 2, source = years_data,
                  fill_color = "MediumSeaGreen")
select_years.add_layout(best_popularity_years_annotation)

# Iremos definir a ferramenta de deslizamento e adicionar ela à segunda figura.
select_years_tool = RangeTool(x_range = years_plot.x_range)
select_years_tool.overlay.fill_color = "MediumAquamarine"
select_years_tool.overlay.fill_alpha = 0.2

select_years.add_tools(select_years_tool)

# Iremos juntar os dois gráficos.
column_years = column(years_plot, select_years)

# Iremos juntar os filtros e o player do spotify em uma coluna.
music_selector = column(row(search_input, column(search_button, align = "end")),
                        row(filter_music), row(Div(text = "<br>")),
                        row(spotify_player),
                        row(Div(text = "<br><br><br><br>")),
                        row(filter_category))

# Iremos juntar as figuras e os filtros ao layout final.
layout = column(row(music_selector, filter_plot),
                row(density_plot, column_years))

curdoc().add_root(layout)
