# Importações do módulo de visualização
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import Select, Button, TextInput, Div, RangeTool, BoxAnnotation
from bokeh.models import NumeralTickFormatter, HoverTool, Label
from bokeh.transform import dodge
from . import read_data
from . import plot_style

# output_file("testando.html")

### A similaridade entre o nome das variáveis das funções se deve ao fato de que
### elas devem ser utilizadas em conjunto.

# Definição de variáveis globais usadas nas funções:

# Definiremos as categorias que serão comparadas na primeira plotagem e usadas na segunda.
categories = ["Danceability", "Energy", "Valence", "Speechiness", "Acousticness"]

# E criaremos um dicionário com as médias das 10 músicas mais ouvidas em cada categoria.
top_ten_categories_mean = {"Danceability": 0.6999, "Energy": 0.5804,
                            "Valence": 0.6048, "Speechiness": 0.06073,
                            "Acousticness": 0.342142}


# Categories plot
################################################################################

# Geraremos a primeira plotagem, que se baseia na comparação de categorias.
def gera_plot_categorias_sillas(path):
    ### Leitura de dados para a primeira plotagem:

    # Primeiro carregaremos todos os nomes de músicas na base de dados (ordenando por vezes escutadas).
    all_music_names = read_data.get_column_observations(path, "Track", sort_column = "Stream")

    # Agora carregaremos os dados da música mais escutada.
    firts_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", all_music_names[0])

    # E separaremos eles em seus valores brutos e a linha dos dados obtida.
    first_music_values, firts_music_row = firts_music_data

    first_music_artist = firts_music_row.data["Artist"][0]

    # Agora iremos adicionar as médias das categorias aos dados:
    categories_means = []

    # Se a coluna for uma categoria, adiciona sua média, se não for, adiciona apenas o seu nome
    for column_name in first_music_values.data["Columns"]:
        column_data = column_name
        if column_data in categories:
            column_data = top_ten_categories_mean[column_name]
            
        categories_means.append(column_data)

    # Adicionaremos uma nova coluna das médias aos dados.
    first_music_values.data["Means"] = categories_means

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
    filter_plot = plot_style.figure_text_generator_sillas(filter_plot)

    # Alteraremos o formato do eixo Y para exibir porcentagem, como todas as categorias
    # vão de 0 à 1, é possível computar seus valores como porcentagens.
    filter_plot.yaxis[0].formatter = NumeralTickFormatter(format = "#0%")

    # Adicionaremos as colunas das médias do top 10.
    médias = filter_plot.vbar(x = dodge("Columns", 0.22, range = filter_plot.x_range),
                    top = "Means", source = first_music_values, width = 0.41,
                    fill_color = "#1ed760", legend_label = "Médias das 10 Músicas mais escutadas no Spotify",
                    line_color = "#535353")
    # Adicionaremos as colunas da música selecionada (a primeira mais escutada).
    selected_music = filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                    top = "Values", source = first_music_values, width = 0.4,
                    fill_color = "DarkViolet", legend_label = all_music_names[0],
                    line_color = "#535353")

    # Removeremos parâmetros desnecessários da legenda para fins estéticos.
    filter_plot.legend.background_fill_alpha = 0
    filter_plot.legend.border_line_alpha = 0

    # Criaremos um hover para as colunas das médias e para as colunas da música selecionada
    # e os adicionaremos ao gráfico.
    hover_medias = HoverTool(renderers = [médias], tooltips = [("Valor", "@Means")])

    hover_musica = HoverTool(renderers = [selected_music], tooltips = [("Valor", "@Values"),
                                                                       ("Artista", first_music_artist)])

    filter_plot.add_tools(hover_medias, hover_musica)

    # E por fim, retornaremos o plot
    return filter_plot

# Density plot
################################################################################

# Geraremos a segunda plotagem que se baseia na distribuição da quantidade de vezes que uma
# música foi ouvida com o quanto de uma categoria ela possui, no caso a escolhida foi Energy.
def gera_plot_densidade_sillas(path, initial_catefory = "Energy"):
    ### Leitura de dados para a segunda plotagem

    # Primeiro carregaremos todos os nomes de músicas na base de dados (ordenando por vezes escutadas).
    all_music_names = read_data.get_column_observations(path, "Track", sort_column = "Stream")

    # Leremos todos os dados
    all_data = read_data.csv_to_columndatasource(path)

    # Obteremos os dados de histograma para a plotagem.
    histogram_data = read_data.histogram_data(path, initial_catefory, proportion_column = "Stream")
    
    # Agora carregaremos os dados da música mais escutada.
    firts_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", all_music_names[0])

    # E separaremos eles em seus valores brutos e a linha dos dados obtida.
    first_music_values, firts_music_row = firts_music_data

    # Criaremos o gráfico de densidade que terá como base a exibição do quanto as
    # categegorias estão presentes em uma música e quantas vezes ela foi ouvida, para atestar
    # a correlação entre as categorias e a quantidade de vezes que elas foram ouvidas.
    density_plot = figure(height=480, width=640, title = f"{initial_catefory} X Vezes tocadas no Spotify (Em bilhões)",
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
    # Daremos destaque a música selecionada do outro gráfico.
    density_plot.star(x = initial_catefory, y = "Stream", source = firts_music_row,
                        size = 18, fill_color = "DarkViolet")

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


# Filters layout
################################################################################


# Função que atualiza a posição da música selecionada a partir do seu nome e nova categoria:
def update_music_star(path, music_name, density_plot):
    # Se já existir uma, ela será deletada.
    if len(density_plot.renderers) > 2:
        del density_plot.renderers[2]

    current_category = density_plot.xaxis.axis_label

    # Obtém os novos dados da música selecionada
    filter_data = read_data.csv_filter_by_name_to_cds(path,
                                            "Track", music_name, lowercase = True)
    # Plota novamente a música selecionada
    density_plot.star(x = current_category, y = "Stream", source = filter_data[1],
                        size = 20, fill_color = "DarkViolet")
    
    return density_plot


# Por fim, geraremos os filtros dos gráficos acima:
def gera_filtros_música(path, filter_plot, density_plot):
    ### Leitura de dados para os filtros:

    # Primeiro carregaremos todos os nomes de músicas na base de dados (ordenando por vezes escutadas).
    all_music_names = read_data.get_column_observations(path, "Track", sort_column = "Stream")
    
    # Agora carregaremos os dados da música mais escutada.
    firts_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", all_music_names[0])

    # E separaremos eles em seus valores brutos e a linha dos dados obtida.
    first_music_values, firts_music_row = firts_music_data

    all_music_names_lower = read_data.get_column_observations(path, "Track", sort_column = "Stream",
                                                                lowercase = True)

    # Criaremos um player do spotify simples com a música mais escutada.
    spotify_player_html = f"""
        <iframe src="https://open.spotify.com/embed?uri={firts_music_row.data["Uri"][0]}"
                width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """
    spotify_player = Div(text = spotify_player_html)

    ### Geração de filtros

    # Adicionaremos uma função que atualiza a música do player dependendo da música que
    # for selecionada.
    def update_spotify_player(spotify_uri):
        spotify_player_html = f"""
        <iframe src="https://open.spotify.com/embed?uri={spotify_uri}"
                width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """
        spotify_player.text = spotify_player_html

    ### Filtro de opções:

    # Adicionaremos a função que atualiza a música selecionada.
    def update_music_selected(attr, old, new):
        new_music = filter_music.value
        # Busca os dados da nova música
        new_data = read_data.csv_filter_by_name_to_cds(path, "Track", new_music, lowercase = True)

        # Atribui os dados à novas variáveis.
        values, row = new_data
        music_uri = row.data["Uri"][0]
        # Deleta as partes do gráfico da última música.
        del filter_plot.renderers[1]
        del filter_plot.legend.items[1]
        
        filter_music.value = new_music
        # Atualiza o título do gráfico.
        filter_plot.title.text = f"Níveis de {new_music}"
        # Atualiza as colunas da música selecionada.
        selected_music = filter_plot.vbar(x = dodge("Columns", -0.22, range = filter_plot.x_range),
                        top = "Values", source = values, width = 0.41,
                        fill_color = "DarkViolet", legend_label = new_music,
                        line_color = "#535353")
        # Recria o hover toll.
        new_hover = HoverTool(renderers = [selected_music],
                    tooltips = [("Valor", "@Values")])
        filter_plot.add_tools(new_hover)

        # Atualiza o player do spotify com a nova música.
        update_spotify_player(music_uri)
        # E indica a música no gráfico de densidade.
        update_music_star(path, new_music, density_plot)

    
    # Criaremos um filtro para poder poder escolher entre todas as músicas disponíveis.
    filter_music = Select(title = "Músicas disponíveis:", options = all_music_names,
                            value = all_music_names[0], height = 35, width = 640,)

    # Adicionaremos a iteratividade da função e da seleção de músicas.
    filter_music.on_change("value", update_music_selected)

    ### Filtro de busca:

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

    ### Layout  final:
    # Por fim, juntaremos tudo em um layout.
    music_selector = column(row(search_input, column(search_button, align = "end")),
                            row(filter_music),
                            row(Div(text = "<br>")),
                            row(spotify_player))
    # E então o retornaremos:
    return music_selector


# Density Plot Filter
################################################################################

def gera_filtros_categorias(path, filter_plot, density_plot):
    ### Leitura de dados:
    # Leremos todos os dados.
    all_data = read_data.csv_to_columndatasource(path)
    
    ### Função que atualiza o gráfico de densidade:

    # Função que atualiza as categorias:
    def update_density_plot(attr, old, new):
        # Recebe a nova categoria e limpa o gráfico.
        new_category = filter_category.value
        density_plot.renderers = []
        # Atualiza os rótulos do gráfico para a nova categoria.
        density_plot.title.text = f"{new_category} X Vezes tocadas no Spotify"
        density_plot.xaxis.axis_label = new_category

        # Gera o novo histograma.
        histogram_data = read_data.histogram_data(path,
                                            new_category, proportion_column = "Stream")
        # E então plota o histograma com a nova categoria.
        density_plot.quad(top = "top", bottom = 0, left = "start", right = "end",
                        fill_color = 'MediumAquamarine', fill_alpha = 0.5, source = histogram_data,
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
        update_music_star(path, filter_plot.title.text[10:], density_plot)
    
    # Criaremos a seleção das categorias:
    filter_category = Select(title = "Tente alterar a categoria selecionada", value = "Energy",
                             options = categories, height = 35, width = 640,)

    # Agora adicionaremos a iteratividade entre a seleção de categorias e sua função de atualização.
    filter_category.on_change("value", update_density_plot)

    # E então retornaremos o filtro:
    return filter_category


def gera_explicacoes_sillas():
    colunas = Div(text = """<h2>Gráfico de colunas com categorias</h2>
    <p>O primeiro gráfico é composto pela comparação entre as categorias Danceability, Energy, Valence, Speechiness, Acousticness.<br>
    Todas as músicas possuem essas características, geradas automaticamente pelo spotify, o objetivo deste gráfico é, através da escolha de
    uma música, com o seletor ao lado do gráfico, fazer uma comparação entre as categorias da música selecionada com a média das categorias das
    top 10 músicas mais ouvidas no Spotify. Como o intuito é uma comparação, foi utilizado um gráfico de colunas lado a lado, a paleta se mantém a mesma,
    com várias inspirações na do spotify, como todas as categorias vão de 0 à 1, é razoável medi-lás em porcentagem.</p>""",
            style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))

    scatter = Div(text = """<h2>Gráfico de scatter plot com histograma</h2>
    <p>O segundo gráfico é composto pela correlação entre a categoria selecionada e o número de vezes ouvidas
    no spotify por músicas, deste modo foi possível trazer um destaque para a música selecionada como uma estrela,
    as categorias disponíveis são as do primeiro gráfico que vão de 0 a 1 e representam o quanto o traço daquela categoria
    está presente na música, já a quantidade de vezes que a música foi escutada está na escala de bilhões, e por isso,
    é possível ver como a distribuição da grande quantidade de músicas na base de dados não é uniforme, por isso foi gerado
    um histograma no fundo com baixa opacidade para ajudar a estimar a densidade das músicas, e a paleta
    não só deste como dos outros gráficos busca trazer um verde referente ao Spotify e um roxo que se destaca em conjunto com o verde.</p>""",
                style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))

    linhas = Div(text = """<h2>Gráfico de linhas</h2>
    <p>O terceira gráfico busca exibir a o crescimento da popularidade médias das músicas lançadas
    por ano, por isso há a escolha do gráfico de linhas para representar esta passagem de tempo,
    além disso uma anotação de destaque foi feita para exibir o aumento da popularidade média
    das músicas a partir do ano de 2017, uma ferramenta de destaque para esta plotagem é a de
    deslizamento, que permite percorrer a linha temporal de maneira dinâmica.</p>""",
                style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))
    
    return column(row(scatter, colunas),row(linhas))

# Função para gerar o layout final da página
def gera_layout_sillas(path):
    # Chamaremos as plotagens:
    plot_músicas = gera_plot_categorias_sillas(path)
    plot_densidade = gera_plot_densidade_sillas(path)
    plot_anos = gera_plot_anos_sillas(path)

    # Seus filtros:
    filtro_musicas = gera_filtros_música(path, plot_músicas, plot_densidade)
    filtro_categorias = gera_filtros_categorias(path, plot_músicas, plot_densidade)
    # Criaremos o layout das músicas:
    
    # As explicações:
    explicacoes = gera_explicacoes_sillas()

    densidade = column(filtro_categorias, plot_densidade)

    # Por fim, juntaremos as filtros, os filtros e as explicações ao layout final.
    layout = column(row(filtro_musicas, plot_músicas),
                    row(densidade, plot_anos),
                    row(explicacoes))
    
    # E retornaremos o layout:
    return layout

# curdoc().add_root(layout)