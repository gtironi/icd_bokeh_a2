# Importações das funções dos módulos

import pandas as pd

from .read_data import columndatasource_plot2_leonardo, columndatasource_plot3_leonardo
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Div
from bokeh.layouts import column, row

# Leitura do arquivo

df = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv")

# Primeira plotagem

# Elaborando a função que cria o objeto do primeiro gráfico

def visualizacao_1_leonardo(datapath):

    
    df = pd.read_csv(datapath)

    # Criação da figura 1

    plot_1 = figure(tools = "xpan", toolbar_location = None)

    # Construindo um gráfico de dispersão

    plot_1.circle(x = "Energy", y = "Danceability", source = df,
              color = "MidnightBlue", size = 1.8)

    # Definindo as informações dos dados que serão visíveis

    tooltips = [
            ("Música", "@Track"),
            ("Artista", "@Artist"),
            ("Álbum", '@Album'),
            ("Visualizações", '@Views')   
           ]

    # Nomeando o gráfico

    plot_1.title.text = "Correlação Entre Energia e Danceabilidade"

    # Posicionando o título do gráfico

    plot_1.title.align = "center"

    # Configurando as dimensões e o fundo da visualização

    plot_1.width = 600
    plot_1.height = 600
    plot_1.xgrid.grid_line_color = None
    plot_1.ygrid.grid_line_color = None
    plot_1.background_fill_color = "Gainsboro"

    # Customização dos eixos

    plot_1.xaxis.axis_label = "Energia"
    plot_1.xaxis.axis_label_text_color = "black"
    plot_1.xaxis.axis_label_text_font = "Arial"
    plot_1.xaxis.axis_label_text_font_size = "12px"

    plot_1.yaxis.axis_label = "Danceabilidade"
    plot_1.yaxis.axis_label_text_color = "black"
    plot_1.yaxis.axis_label_text_font = "Arial"
    plot_1.yaxis.axis_label_text_font_size = "12px"

    # Adicionando as informações ao gráfico

    plot_1.add_tools(HoverTool(tooltips=tooltips))

    # Retornando a primeira visualização

    return plot_1

# plot_1_leonardo = visualizacao_1_leonardo(df)

################################################################################

# Segunda plotagem

# Inserindo o CDS em uma variável

df_2 = columndatasource_plot2_leonardo('visualizacoes/data/spotify_youtube_year.csv')

# Elaborando a função que cria o objeto do segundo gráfico

def visualizacao_2_leonardo(datapath):
    
    df_2 = columndatasource_plot2_leonardo(datapath)

    # Contruindo uma nova coluna de curtidas em milhões

    df["Curtidas"] = df["Likes"] / 1000000

    # Agrupamento das 10 músicas com mais curtidas

    df_duration_per_track = df.groupby("Track")["Curtidas"].mean().sort_values(ascending = False).head(10).reset_index()

    # Ordenando de forma decrescente

    df_duration_per_track = df_duration_per_track.sort_values(by = "Curtidas", ascending = True)

    # Criando um player da Música Despacito no Spotify

    spotify_player_html = f"""
    <iframe src="https://open.spotify.com/embed?uri=spotify:track:6habFhsOp2NvshLv26DqMb"
           width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """

    # Inserindo o player na página HTML

    spotify_player = Div(text=spotify_player_html)

    # Configurando as dimensões

    spotify_player.width = 640
    spotify_player.height = 180

    # Criação da figura 2

    plot_2 = figure(tools = "xpan", toolbar_location = None, y_range = df_duration_per_track["Track"].values)

    # Construindo um gráfico de barras horizontais

    plot_2.hbar(y = "Track", right = "Curtidas", height=0.7, source = df_2,
            color = "MediumBlue")

    # Nomeando o gráfico

    plot_2.title.text = "As 10 músicas com mais curtidas no YouTube (em milhões)"

    # Posicionando o título do gráfico

    plot_2.title.align = "left"

    # Configurando as dimensões e o fundo das visualizações

    plot_2.width = 640
    plot_2.height = 480
    plot_2.ygrid.grid_line_color = None
    plot_2.background_fill_color = "Gainsboro"

    # Customização dos eixos

    plot_2.xaxis.axis_label_text_color = "black"
    plot_2.xaxis.axis_label_text_font = "Arial"
    plot_2.xaxis.axis_label_text_font_size = "12px"

    plot_2.yaxis.axis_label_text_color = "black"
    plot_2.yaxis.axis_label_text_font = "Arial"
    plot_2.yaxis.axis_label_text_font_size = "12px"

    # Retornando a segunda visualização

    return column(spotify_player, plot_2)

# plot_2_leonardo = visualizacao_2_leonardo(df_2)

################################################################################

# Terceira plotagem

# Inserindo o CDS em uma variável

df_3 = columndatasource_plot3_leonardo('visualizacoes/data/spotify_youtube_year.csv')

def visualizacao_3_leonardo(datapath):

    # Contruindo uma nova coluna de curtidas em milhões

    df["Curtidas"] = df["Likes"] / 1000000

    # Média de curtidas por ano (em milhões)

    likes_by_year = df.groupby(["release_date"])["Curtidas"].mean() 

    # Transformando a pd.Series em uma DataFrame

    likes_by_year = pd.DataFrame(likes_by_year)

    # Transformando a pd.Series em uma DataFrame

    likes_by_year = pd.DataFrame(likes_by_year)

    # Criação da figura 3

    plot_3 = figure(tools = "xpan", toolbar_location = None)

    # Construindo um gráfico de linhas

    plot_3.line(x = "release_date", y = "Curtidas", source = df_3, line_width=2)

    # Inserindo os pontos que representam os valores das variáveis 

    plot_3.circle(x = "release_date", y = "Curtidas", source = df_3)

    # Nomeando o gráfico

    plot_3.title.text = "Média de curtidas (em milhões)"

    # Posicionando o título do gráfico

    plot_3.title.align = "center"

    # Configurando as dimensões e o fundo das visualizações

    plot_3.width = 640
    plot_3.height = 480
    plot_3.xgrid.grid_line_color = None
    plot_3.ygrid.grid_line_color = None
    plot_3.background_fill_color = "Gainsboro"

    # Customização dos eixos

    plot_3.xaxis.axis_label_text_color = "black"
    plot_3.xaxis.axis_label_text_font = "Arial"
    plot_3.xaxis.axis_label_text_font_size = "12px"

    plot_3.yaxis.axis_label_text_color = "black"
    plot_3.yaxis.axis_label_text_font = "Arial"
    plot_3.yaxis.axis_label_text_font_size = "12px"

    # Retornando a terceira visualização

    return plot_3

# plot_3_leonardo = visualizacao_3_leonardo(df_3)

# Apresentação das análises 
def gera_textos_leo():
    # Comentários sobre a primeira visualização

    text_1 = Div(text = """<h1> Spotify e YouTube </h1>
    <p> A partir de uma base de dados, do Kaggle, sobre músicas do Spotify e Youtube, foram elaboradas todas as 
    visualizações dessa página. <p>
    <h2> Energia x Danceabilidade </h2>
    <p> A partir de duas variáveis, danceabilidade e energia, produziu-se um gráfico de dispersão.
    A danceabilidade representa o quão dançante é a música no intervalo de 1 a 0 e a 
    energia indica o quão energizada uma música está no intervalo de 1 a 0. 
    Pelo gráfico, pode-se perceber que a danceabilidade de uma música tende a 
    aumentar conforme o aumento da sua energia.
    Além disso, ao passar o cursor do mouse por cima de algum ponto, quatro dados da música 
    são disponibilizados: música; artista; álbum; visualizações. <p>
    """,
    style = {"text-align": "center", "font-size": "16px"}, width = 430, align = "center", margin = (10, 0, 10, 30))

    # Comentários sobre a segunda visualização

    text_2 = Div(text = """
    <h2> Ranking de Curtidas </h2>
    <p> Uma das principais formas de avaliar uma música é por meio da quantidade de 
    curtidas. 
    Nesse caso, o gráfico de barras é muito útil, pois, com o seu esboço, torna-se 
    possível a construção de um ranking.
    Como a base de dados possui a quantidade de curtidas das músicas no YouTube,
    o top 10 das músicas com mais curtidas pode ser representado em um gráfico de barras.
    Para isso, criou-se uma nova coluna de curtidas em milhões.
    Assim, as 10 músicas com mais curtidas, no YouTube, foram organizadas em ordem decrescente.
    Com essas 10 músicas, construiu-se um gráfico de barras horizontais.
    No gráfico, fica nítido que a música com mais curtidas é Despacito.
    Assim, elaborou-se um player da música Despacito no Spotify. <p>
    """,
    style = {"text-align": "center", "font-size": "16px"}, width = 430, align = "center", margin = (10, 0, 10, 30))

    # Comentários sobre a terceira visualização

    text_3 = Div(text = """
    <h2> Média de Curtidas por Ano </h2>
    <p> Quando de trata de dados numéricos ao longo do tempo, a melhor opção de
    esboço é o gráfico de linhas.
    Na base de dados, existe uma coluna, que possui as datas de lançamento das músicas, chamada de release_date.
    Por outro lado, anteriormente, criou-se uma coluna de curtidas em milhões.
    Sob essa perspectiva, a média de curtidas por ano foi calculada mediante essa coluna.
    Dessa forma, plotou-se um gráfico de linhas com a média de curtidas das músicas, no Youtube, ao longo dos anos.
    Pelo gráfico, o leitor pode observar os aumentos e as quedas em determinados intervalos de tempo,
    o que possibilita a realização de comparações entre períodos. <p>
    """,
    style = {"text-align": "center", "font-size": "16px"}, width = 430, align = "center", margin = (10, 0, 10, 30))

    return [text_1, text_2, text_3]


def gera_layout_leonardo(path):
    """ Gera o layout das visualizações"""
    plot_1_leonardo = visualizacao_1_leonardo(path)
    plot_2_leonardo = visualizacao_2_leonardo(path)
    plot_3_leonardo = visualizacao_3_leonardo(path)

    comentarios = gera_textos_leo()
    text_1 = comentarios[0]
    text_2 = comentarios[1]
    text_3 = comentarios[2]

    # Layout da imagem

    layout = column(row(plot_1_leonardo, column(text_1)), row(plot_2_leonardo, text_2), row(plot_3_leonardo, text_3))

    # Retornando o layout

    return layout

