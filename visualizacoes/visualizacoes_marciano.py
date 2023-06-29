# Arquivo para os códigos das  visualizacoes

# Importando os módulos utilizados
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.annotations import BoxAnnotation
from bokeh.models import HoverTool, ColumnDataSource


########################################################################################################################

data = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv") # Lendo o .csv como um data frame do pandas

########################################################################################################################
# Primeiro gráfico: Scatter plot Liveness X Energy #


color = [] # Criando lista vazia para posteriormente tranformar em coluna que define a cor dos glifos.

for each_float in data["Liveness"]: # Loop para percorrer a coluna Liveness, e dependendo se o valor é maior que 0.8
     if each_float >= 0.8:             # é maior ou menor que 0.8, adiciona a palavra Red na lista vazia criada acima.
         color.append("Red")
     else:
         color.append("Gray")

data["color"] = color # Criando a coluna que irá definir a cor dos glifos baseada na lista criada acima

plot_1 = figure(width=600, height = 600, title = "Liveness X Energy") # Criando a figura do gráfico 2

data_source_1 = ColumnDataSource(data) # Tranforma o data frame em ColumDataSource

plot_1.circle(x = "Liveness", y = "Energy", source = data_source_1, color = "color", alpha = 0.4, size = 8) #Criando scatter plot com os dados do data_source_1

box_annotation_4 = BoxAnnotation(left=0.8, right=1, fill_color = "Red", fill_alpha = 0.2) # Criando retângulo e dicionando ao gráfico
plot_1.add_layout(box_annotation_4) 

tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre os glifos
    ('Música', '@Track'),
    ('Artista', '@Artist'),
    ('Álbum', '@Album'),
    ('Streams', '@Stream')]
plot_1.add_tools(HoverTool(tooltips=tooltips))



########################################################################################################################
# Segundo gráfico: Duração das músicas X Anos

plot_2 = figure(width=600, height = 600) # Criando a figura do gráfico 1
 
data["Duration_s"] = data["Duration_ms"]/1000 # Mudando a coluna Duration_ms para segundos (dividindo por 1000)

duration_by_year = pd.DataFrame(data.groupby(["release_date"])["Duration_s"].mean()) # Agrupando por ano de lançamento e calculando a média de
                                                                                     # duração das músicas por ano em um pd.Series transformado em DataFrame

count_by_year = pd.DataFrame(data.groupby(["release_date"])["Track"].count())  # Agrupando por ano de lançamento e contando o número de
                                                                               # músicas por ano em um pd.Series transformado em DataFrame


data_by_year = duration_by_year                         # Linhas para juntar os DataFrames em um só
data_by_year["Track Count"] = count_by_year["Track"]

data_by_year_filtered = data_by_year[data_by_year['Track Count'] > 90] # Filtrando o DataFrame para os anos com mais de 90 músicas

data_source_2 = ColumnDataSource(data_by_year_filtered) # Transformando em ColumnDataSource

plot_2.line(x = "release_date", y = "Duration_s", source = data_source_2) # Criando o line plot com os dados do ColumnDataSource

tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre pontos da linha
    ('Ano', '@release_date'),
    ('Duração Média', '@Duration_s'),
    ]
plot_2.add_tools(HoverTool(tooltips=tooltips))



########################################################################################################################

# Terceiro gráfico: Top 30 artistas
data = data.dropna(subset=['Stream']) # Removendo as músicas que não possuiam o númeoro de streams

stream_by_artist = pd.DataFrame(data.groupby(["Artist"])["Stream"].mean().sort_values().tail(30)) # Agrupando por artista, calulando a média de streams,
                                                                                                  # ordenando da menor para a maior nº de streams e deixando
                                                                                                  # somente as últimas 30 linhas do data frame.

data_source_3 = ColumnDataSource(stream_by_artist) # Transformando em ColumnDataSource

plot_3 = figure(y_range=stream_by_artist.index.tolist(), height=600, width=600, title="Top 30 Artistas Mais Ouvidos") # Criando a figura do gráfico 3

plot_3.hbar(y='Artist', right='Stream', height=0.8, source=data_source_3) # Criando o horizontal bar plot com os dados co ColumnDataSource

tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre as barras
    ('Nº Médio de Streams', '@Stream'),
    ]
plot_3.add_tools(HoverTool(tooltips=tooltips))


