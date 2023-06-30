# Importações do módulo de visualização
from bokeh.io import save, show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Div, RangeTool, BoxAnnotation
from bokeh.models import NumeralTickFormatter, HoverTool, Label
from bokeh.transform import dodge
import read_data
import plot_style

### A similaridade entre o nome das variáveis das funções se deve ao fato de que
### elas devem ser utilizadas em conjunto.

# Categories plot
################################################################################

# Geraremos a primeira plotagem, que se baseia na comparação das categorias entre
# a música mais escutada e a mais popular.
def gera_plot_categorias_sillas(path):
    ### Leitura de dados para a primeira plotagem:

    # Obteremos a música mais ouvida do Spotify
    top_listened_music = read_data.csv_get_top_names(path, "Track", sort_column = "Stream", num = 1)
    # Agora carregaremos os dados dela.
    top_listened_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", top_listened_music)

    # E separaremos eles em seus valores brutos e a linha dos dados obtida.
    top_listened_music_values, top_listened_music_row = top_listened_music_data

    top_listened_artist = top_listened_music_row.data["Artist"][0]

    # E faremos o mesmo com a música mais popular, obteremos ela e separaremos seus dados.
    top_popularity_music = read_data.csv_get_top_names(path, "Track", sort_column = "popularity", num = 1)

    top_popularity_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", top_popularity_music)
    top_popularity_music_values, top_popularity_music_row = top_popularity_music_data

    top_popularity_artist = top_popularity_music_row.data["Artist"][0]
    
    # Definiremos as categorias que serão comparadas.
    categories = ["Danceability", "Energy", "Valence", "Speechiness", "Acousticness"]

    # Deste modo criaremos a primeira plotagem, que irá comparar os níveis por categoria
    # da música mais escutada e a música mais popular.
    filter_plot = figure(height=480, width=640, title = f"Comparação entre a música mais ouvida, {top_listened_music},\ncom a mais popular, {top_popularity_music}",
                        tools = "xpan", toolbar_location = None,
                        x_range = categories, y_range = [0, 1.15])

    # Removeremos alguns parâmetros para fins estéticos.
    filter_plot.xaxis.axis_label = None
    filter_plot.xgrid.grid_line_color = None
    # Adicionaremos os intervalos do eixo Y.
    filter_plot.yaxis.ticker = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    # Iremos carregar o tema pré definido de rótulos e cor de fundo.
    filter_plot = plot_style.figure_text_generator_sillas(filter_plot)

    # Alteraremos o formato do eixo Y para exibir porcentagem, como todas as categorias
    # vão de 0 à 1, é possível computar seus valores como porcentagens.
    filter_plot.yaxis[0].formatter = NumeralTickFormatter(format = "#0%")

    # Adicionaremos as colunas da música mais popular.
    popular = filter_plot.vbar(x = dodge("Columns", 0.22, range = filter_plot.x_range),
                    top = "Values", source = top_popularity_music_values, width = 0.41,
                    fill_color = "#1ed760", legend_label = top_popularity_music,
                    line_color = "#535353")
    # Adicionaremos as colunas da música mais ouvida.
    streamed = filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                    top = "Values", source = top_listened_music_values, width = 0.4,
                    fill_color = "DarkViolet", legend_label = top_listened_music,
                    line_color = "#535353")

    # Removeremos parâmetros desnecessários da legenda para fins estéticos.
    filter_plot.legend.background_fill_alpha = 0
    filter_plot.legend.border_line_alpha = 0

    # Criaremos um hover para as colunas das médias e para as colunas da música selecionada
    # e os adicionaremos ao gráfico.
    hover_popularidade = HoverTool(renderers = [popular, streamed], tooltips = [("Valor", "@Values"),
                                                                           ("Artista", top_popularity_artist)])
    
    hover_streamed = HoverTool(renderers = [streamed], tooltips = [("Valor", "@Values"),
                                                                    ("Artista", top_listened_artist)])


    filter_plot.add_tools(hover_popularidade, hover_streamed)

    # E por fim, retornaremos o plot
    return filter_plot

# Density plot
################################################################################

# Geraremos a segunda plotagem que se baseia na distribuição da quantidade de vezes que uma
# música foi ouvida com o quanto de uma categoria ela possui, no caso a escolhida foi Energy.
def gera_plot_densidade_sillas(path, initial_catefory = "Energy"):
    ### Leitura de dados para a segunda plotagem

    # Leremos todos os dados
    all_data = read_data.csv_to_columndatasource(path)

    # Obteremos os dados de histograma para a plotagem.
    histogram_data = read_data.histogram_data(path, initial_catefory, proportion_column = "Stream")

    # Criaremos o gráfico de densidade que terá como base a exibição do quanto as
    # categegorias estão presentes em uma música e quantas vezes ela foi ouvida, para atestar
    # a correlação entre as categorias e a quantidade de vezes que elas foram ouvidas.
    density_plot = figure(height=480, width=640, title = "Nível de Energia X Vezes tocadas no Spotify (Em bilhões)",
                        tools = "xpan", toolbar_location = None,
                        x_range = [0, 1], y_range = [0, 3500000000])

    # Formataremos o eixo X.
    density_plot.xaxis.axis_label = initial_catefory
    density_plot.xaxis.ticker = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # Agora o eixo Y.
    density_plot.yaxis.axis_label = "Número de vezes tocadas no Spotify"
    density_plot.yaxis.ticker = [0, 500000000, 1000000000, 1500000000, 2000000000, 2500000000, 3000000000, 3500000000]
    # Removeremos as linhas de grid.
    density_plot.xgrid.grid_line_color = None
    density_plot.ygrid.grid_line_color = None

    # Utilizaremos o tema pré definido.
    density_plot = plot_style.figure_text_generator_sillas(density_plot)

    # Alteraremos o formato dos eixos, o eixo x novamente irá de 0 à 1 pois é uma das categorias,
    # entretanto o eixo Y chega à escala de bilhões.
    density_plot.xaxis.formatter = NumeralTickFormatter(format = "#0%")
    density_plot.yaxis.formatter = NumeralTickFormatter(format = "0.#a")

    # Geraremos o histograma da distribuição à partir dos dados, o objetivo é exibir o
    # agrupamento dos dados na enorme quantidade de pontos gerada.
    density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                    fill_color = 'MediumAquamarine', fill_alpha = 0.5, source = histogram_data,
                    line_color = "#535353")
    # Agora geraremos todas as músicas em um scatter plot onde o eixo X é a categoria
    # e o Y é a quantidade de vezes ouvidas.
    musics = density_plot.circle(x = initial_catefory, y = "Stream", size = 6, source = all_data,
                        fill_color = "#1DB954", line_color = "DarkGreen",
                        fill_alpha = 0.7)
    
    ### Density plot Annotations
    # Iremos adicionar anptações para destacar
    energy_level_annotation = BoxAnnotation(left = 0.39, right = 0.81, bottom = 2200000000, top = 3450000000,
                        fill_alpha = 0.3, fill_color = 'BlueViolet')

    density_plot.add_layout(energy_level_annotation)
    # Iremos adicionar um texto simples indicando o motivo da caixa de anotações.
    energy_level_annotation_label = Label(x = 0.22, y = 2900000000,
                        text = "Músicas mais ouvidas\npossuem níveis de energia\nmédios maiores.",
                        text_align = "center", text_font_size = "14px", text_font = "Arial")

    density_plot.add_layout(energy_level_annotation_label)


    # Adicionaremos um hover com os dados das músicas ao gráfico.
    musics_hover = HoverTool(renderers = [musics],
                    tooltips = [("Música", "@Track"), ("Artista", "@Artist")])

    density_plot.add_tools(musics_hover)
    # E por fim, retornaremos o gráfico obtido.
    return density_plot


# Mean popularity by Year Plot
################################################################################

# Adicionaremos a função que gera a plotagem dos anos
def gera_plot_anos_sillas(path):
    ### Leitura dos dados para a terceira plotagem:

    # Obteremos os dados dos anos e da popularidade média por ano.
    years_data = read_data.get_statistic_by_year(path, "release_date", "popularity")

    # Geraremos a figura dos anos.
    years_plot = figure(title = "Crescimento da Popularidade média das músicas por Ano",
                        height = 350, width = 640, tools = "xpan", toolbar_location = None,
                        x_range = [2001, 2021], y_range = [0, 100],
                        x_axis_label = "Anos", y_axis_label = "Popularidade Média",)
    # Adicionaremos o tema pré definido à figura.
    years_plot = plot_style.figure_text_generator_sillas(years_plot)
    # Removeremos o grid do eixo X para fins estéticos.
    years_plot.xgrid.grid_line_color = None
    # Adicionaremos os intervalos do eixo Y.
    years_plot.yaxis.ticker = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # Geraremos o gráfico de linhas temporal.
    line_years = years_plot.line(x = "Years", y = "Values", source = years_data,
                    line_color = "LightSeaGreen")
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
                        text_align = "center", text_font_size = "14px", text_font = "Arial")

    years_plot.add_layout(best_popularity_years_label)

    ### Year plot Slider

    # Iremos criar uma figura para poder percorrer pelos anos de maneira dinâmica.
    select_years = figure(title = "Arraste para selecionar os anos desejados da observação",
                        height = 130, width = 640, y_range = years_plot.y_range,
                        y_axis_type = None, tools = "", toolbar_location = None)

    # Iremos passar alguns parâmetros estéticos à essa figura.
    select_years.background_fill_color="GhostWhite"
    select_years.xgrid.grid_line_color = None
    select_years.ygrid.grid_line_color = None

    # E por fim, alteraremos o seu título.
    select_years.title.text_color = "Black"
    select_years.title.text_font = "Arial Black"
    select_years.title.align = "center"

    # Iremos fazer a nova figura semelhante à original em termos gráficos.
    select_years.line(x = "Years", y = "Values", source = years_data,
                    line_color = "LightSeaGreen")
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

    # E então retornálos juntos.
    return column_years

def gera_spotify_player(path):
    ### Leitura de dados para o player:

    # Obteremos a música mais ouvida do Spotify
    top_listened_music = read_data.csv_get_top_names(path, "Track", sort_column = "Stream", num = 1)
    # Agora carregaremos os dados dela.
    top_listened_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", top_listened_music)

    # E separaremos eles em seus valores brutos e a linha dos dados obtida.
    top_listened_music_values, top_listened_music_row = top_listened_music_data

    top_listened_uri = top_listened_music_row.data["Uri"][0]

    # E faremos o mesmo com a música mais popular, obteremos ela e separaremos seus dados.
    top_popularity_music = read_data.csv_get_top_names(path, "Track", sort_column = "popularity", num = 1)

    top_popularity_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", top_popularity_music)
    top_popularity_music_values, top_popularity_music_row = top_popularity_music_data

    top_popularity_uri = top_popularity_music_row.data["Uri"][0]
    
    
    # Criaremos um player do spotify simples com a música mais escutada.
    spotify_player_1_html = f"""
        <iframe src="https://open.spotify.com/embed?uri={top_listened_uri}"
                width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """
    # E renderizaremos o player
    spotify_player_top_listened = Div(text = spotify_player_1_html)

    # E agora para a mais popular
    spotify_player_2_html = f"""
        <iframe src="https://open.spotify.com/embed?uri={top_popularity_uri}"
                width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """
    
    spotify_player_top_popular = Div(text = spotify_player_2_html)

    # Assim devolveremos os dois players em sequência.
    return column(row(spotify_player_top_listened), row(spotify_player_top_popular))


def gera_explicacoes_sillas():
    colunas = Div(text = """<h2>Gráfico de colunas com categorias</h2>
    <p>O primeiro gráfico é composto pela comparação entre as categorias Danceability, Energy, Valence, Speechiness, Acousticness.<br>
    Todas as músicas possuem essas características, geradas automaticamente pelo spotify, o objetivo deste gráfico é, 
    fazer uma comparação entre a música mais ouvida, Bliding Lights, com a música mais popular Peaches. Como o intuito é uma comparação, foi utilizado um gráfico de colunas lado a lado, e 
    como todas as categorias vão de 0 à 1, é razoável medí-las em porcentagem, 
    a paleta se mantém a mesma, com várias inspirações na do spotify..</p>""",
            style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))
    scatter = Div(text = """<h2>Gráfico de scatter plot com histograma</h2>
    <p>O segundo gráfico é composto pela correlação entre o nível de energia da música e o número de vezes ouvidas
    no spotify por músicas. <br> 
A energia é um traço da música que varia de 0 à 1, e por isso foi medida em porcetagem, já a quantidade de vezes que a música foi escutada está na escala de bilhões, e por isso,
    é possível ver como a distribuição da grande quantidade de músicas na base de dados não é uniforme, por isso foi gerado
    um histograma no fundo com baixa opacidade para ajudar a estimar a densidade das músicas, a anotação se deve ao fato de que músicas que foram escutadas diversas vezes possuem níveis de energia mais elevados,
        a paleta não só deste como dos outros gráficos busca trazer um verde referente ao Spotify e um roxo
        que se destaca em conjunto com o verde,</p>""",
                style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))

    linhas = Div(text = """<h2>Gráfico de linhas</h2>
    <p>O terceira gráfico busca exibir a o crescimento da popularidade médias das músicas lançadas
    por ano, por isso há a escolha do gráfico de linhas para representar esta passagem de tempo,
    além disso uma anotação de destaque foi feita para exibir o aumento da popularidade média
    das músicas a partir do ano de 2017, uma ferramenta de destaque para esta plotagem é a de
    deslizamento, que permite percorrer a linha temporal de maneira dinâmica.</p>""",
                style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))
    
    return row(column(scatter), column(colunas, linhas))



gráfico_músicas = gera_plot_categorias_sillas("visualizacoes/data/spotify_youtube_year.csv")
gráfico_densidade = gera_plot_densidade_sillas("visualizacoes/data/spotify_youtube_year.csv")
gráfico_anos = gera_plot_anos_sillas("visualizacoes/data/spotify_youtube_year.csv")
palyer = gera_spotify_player("visualizacoes/data/spotify_youtube_year.csv")
explicacoes = gera_explicacoes_sillas()


layout = column(row(palyer, gráfico_músicas),
                row(gráfico_densidade, gráfico_anos),
                row(explicacoes))

show(layout)
