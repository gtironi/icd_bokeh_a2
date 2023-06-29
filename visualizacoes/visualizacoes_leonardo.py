# Importações das funções dos módulos

import pandas as pd

import read_data
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, save, show
from bokeh.models import HoverTool, ColumnDataSource, Div
from bokeh.layouts import column, row

# Leitura do arquivo

df = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv")

# Primeira plotagem

# Criação da figura 1

plot_1 = figure()

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

#Customização dos eixos

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

"""
A danceabilidade representa o quão dançante é a música no intervalo de 1 a 0 e a 
energia indica o quão energizada uma música está no intervalo de 1 a 0. A partir 
dessas duas variáveis, produziu-se um gráfico de dispersão.
Pelo gráfico, pode-se perceber que a danceabilidade de uma música tende a 
aumentar conforme o aumento da sua energia.
"""

################################################################################

# Segunda plotagem

# Contruindo nova coluna de curtidas em milhões

df["Curtidas"] = df["Likes"] / 1000000

# Agrupamento das 10 músicas com mais curtidas

df_duration_per_track = df.groupby("Track")["Curtidas"].mean().sort_values(ascending = False).head(10).reset_index()

# Ordenando de forma decrescente

df_duration_per_track = df_duration_per_track.sort_values(by = "Curtidas", ascending = True)

# Gerando um ColumnDataSource

to_cds = ColumnDataSource(df_duration_per_track)

# Criação da figura 2

plot_2 = figure(y_range = df_duration_per_track["Track"].values)

plot_2.hbar(y = "Track", right = "Curtidas", height=0.7, source = to_cds,
            color = "MediumBlue")

# Nomeando o gráfico

plot_2.title.text = "As 10 músicas com mais curtidas no YouTube (em milhões)"

# Posicionando o título do gráfico

plot_2.title.align = "left"

# Configurando as dimensões e o fundo das visualizações

plot_2.width = 600
plot_2.height = 600
plot_2.ygrid.grid_line_color = None
plot_2.background_fill_color = "Gainsboro"

#Customização dos eixos

plot_2.xaxis.axis_label_text_color = "black"
plot_2.xaxis.axis_label_text_font = "Arial"
plot_2.xaxis.axis_label_text_font_size = "12px"

plot_2.yaxis.axis_label_text_color = "black"
plot_2.yaxis.axis_label_text_font = "Arial"
plot_2.yaxis.axis_label_text_font_size = "12px"

"""
Uma das principais formas de avaliar uma música é por meio da quantidade de 
curtidas. 
Nesse caso, o gráfico de barras é muito útil, pois, com o seu esboço, torna-se 
possível a construção de um ranking.
Portanto, construiu-se um gráfico de barras das 10 músicas com mais curtidas no
YouTube.
"""

################################################################################

# Terceira plotagem

# Média de curtidas por ano (em milhões)

likes_by_year = df.groupby(["release_date"])["Curtidas"].mean() 

# Transformando pd.Series em um DataFrame

likes_by_year = pd.DataFrame(likes_by_year)

# Gerando um ColumnDataSource

to_cds = ColumnDataSource(likes_by_year)

# Criação da figura 3

plot_3 = figure()

plot_3.line(x = "release_date", y = "Curtidas", source = to_cds, line_width=2)

# Nomeando o gráfico

plot_3.title.text = "Média de curtidas (em milhões)"

# Posicionando o título do gráfico

plot_3.title.align = "center"

# Configurando as dimensões e o fundo das visualizações

plot_3.width = 600
plot_3.height = 600
plot_3.xgrid.grid_line_color = None
plot_3.ygrid.grid_line_color = None
plot_3.background_fill_color = "Gainsboro"

#Customização dos eixos

plot_3.xaxis.axis_label_text_color = "black"
plot_3.xaxis.axis_label_text_font = "Arial"
plot_3.xaxis.axis_label_text_font_size = "12px"

plot_3.yaxis.axis_label_text_color = "black"
plot_3.yaxis.axis_label_text_font = "Arial"
plot_3.yaxis.axis_label_text_font_size = "12px"

# Exibição das visualizações

"""
O gráfico de linha acima apresenta a média de curtidas das músicas, contidas na
base dados, no Youtube ao longo dos anos. Assim, o leitor pode observar os
aumentos e as quedas em determinados intervalos de tempo. 
"""

show(row(plot_1, plot_2, plot_3))