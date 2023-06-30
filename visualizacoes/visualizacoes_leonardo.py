# Importações das funções dos módulos

import pandas as pd

import read_data
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, save, show
from bokeh.models import HoverTool, ColumnDataSource, Div
from bokeh.layouts import column, row, gridplot

# Leitura do arquivo

df = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv")

# Primeira plotagem

# Elaborando a função que cria o objeto do primeiro gráfico

def visualizacao_1_leonardo(datapath):

    # Criação da figura 1

    plot_1 = figure()

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

plot_1_leonardo = visualizacao_1_leonardo(df)

################################################################################

# Segunda plotagem

# Contruindo nova coluna de curtidas em milhões

df["Curtidas"] = df["Likes"] / 1000000

# Agrupamento das 10 músicas com mais curtidas

df_duration_per_track = df.groupby("Track")["Curtidas"].mean().sort_values(ascending = False).head(10).reset_index()

# Ordenando de forma decrescente

df_duration_per_track = df_duration_per_track.sort_values(by = "Curtidas", ascending = True)

def columndatasource_plot2_leonardo(datapath):
    """ Gera um objeto ColumnDataSource a partir de um arquivo .csv """
    """ O objeto será utilizado para elaborar a segunda visualização """

    # Leitura do arquivo

    df = pd.read_csv(datapath)

    # Gerando um ColumnDataSource

    to_cds_2 = ColumnDataSource(df_duration_per_track)

    # Retornando a CDS da segunda visualização

    return to_cds_2

# Inserindo o CDS em uma variável

df_2 = columndatasource_plot2_leonardo('visualizacoes/data/spotify_youtube_year.csv')

# Elaborando a função que cria o objeto do segundo gráfico

def visualizacao_2_leonardo(datapath):

    # Criando um player da Música Despacito no Spotify

    spotify_player_html = f"""
    <iframe src="https://open.spotify.com/embed?uri=spotify:track:6habFhsOp2NvshLv26DqMb"
           width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """

    # Inserindo o player na página HTML

    spotify_player = Div(text=spotify_player_html)

    # Configurando as dimensões

    spotify_player.width = 640
    spotify_player.height = 360

    # Criação da figura 2

    plot_2 = figure(y_range = df_duration_per_track["Track"].values)

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

    return row(spotify_player, plot_2)

plot_2_leonardo = visualizacao_2_leonardo(df_2)

################################################################################

# Terceira plotagem

# Média de curtidas por ano (em milhões)

likes_by_year = df.groupby(["release_date"])["Curtidas"].mean() 

# Transformando a pd.Series em uma DataFrame

likes_by_year = pd.DataFrame(likes_by_year)

# Transformando a pd.Series em uma DataFrame

likes_by_year = pd.DataFrame(likes_by_year)

def columndatasource_plot3_leonardo(datapath):
    """ Gera um objeto ColumnDataSource a partir de um arquivo .csv """
    """ O objeto será utilizado para elaborar a terceira visualização """

    # Leitura do arquivo

    df = pd.read_csv(datapath)

    # Gerando um ColumnDataSource

    to_cds_3 = ColumnDataSource(likes_by_year)

    # Retornando a CDS da terceira visualização

    return to_cds_3

# Inserindo o CDS em uma variável

df_3 = columndatasource_plot3_leonardo('visualizacoes/data/spotify_youtube_year.csv')

def visualizacao_3_leonardo(datapath):

    # Criação da figura 3

    plot_3 = figure()

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

plot_3_leonardo = visualizacao_3_leonardo(df_3)

# Layout da imagem

layout = column((plot_2_leonardo), row(plot_1_leonardo, plot_3_leonardo))

# Exibição do layout

show(layout)