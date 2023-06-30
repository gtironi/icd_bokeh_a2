# Arquivo para os códigos das  visualizacoes

# Importando os módulos utilizados
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models.annotations import BoxAnnotation
from bokeh.models import HoverTool, ColumnDataSource, Label, RangeTool, LabelSet
from bokeh.layouts import column, row
import read_data


########################################################################################################################
# Primeiro gráfico: Scatter plot Liveness X Energy #
data_source_1 = read_data.marciano_plot1_data("visualizacoes/data/spotify_youtube_year.csv") # Função para gerar os dados do plot 1

plot_1 = figure(width=600, height = 600, tools = "box_zoom, pan, reset, save, wheel_zoom") # Criando a figura do gráfico 2

plot_1.circle(x = "Liveness", y = "Energy", source = data_source_1, color = "color", alpha = 0.4, size = 8) #Criando scatter plot com os dados do data_source_1

plot_1.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
plot_1.background_fill_alpha = 0.1 # Definindo transparência do fundo do gráfico

# Definindo o Título
plot_1.title.text = "Liveness X Energy"
plot_1.title.text_color = "Black"
plot_1.title.text_font = "Arial Black"
plot_1.title.text_font_size = "30px"
plot_1.title.align = "center"

# Legenda do eixo X
plot_1.xaxis.axis_label = "Liveness" # Definindo texto
plot_1.xaxis.axis_label_text_font = 'Arial Black' # Definindo fonte 
plot_1.xaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
plot_1.xaxis.axis_label_text_color = 'Black' # Definindo cor da letra

# Legenda do eixo Y
plot_1.yaxis.axis_label = "Energy" # Definindo texto
plot_1.yaxis.axis_label_text_font = 'Arial Black' # Definindo fonte
plot_1.yaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
plot_1.yaxis.axis_label_text_color = 'Black' # Definindo cor da letra

box_annotation = BoxAnnotation(left=0.8, right=1, fill_color = "Blue", fill_alpha = 0.15) # Criando retângulo e adicionando ao gráfico
plot_1.add_layout(box_annotation) 

annotation = Label(x=0.775, y=0.1, text="Músicas ao vivo", text_font_size="10pt",text_font = "Arial Black"   # Criando uma anotação do gráfico
                   , text_color="Blue", background_fill_alpha=0.0)                                 
plot_1.add_layout(annotation)                                                                            # Adicionando anotação por cima do gráfico

tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre os glifos
    ('Música', '@Track'),
    ('Artista', '@Artist'),
    ('Álbum', '@Album'),
    ('Streams', '@Stream')]
plot_1.add_tools(HoverTool(tooltips=tooltips))

########################################################################################################################
# Segundo gráfico: Duração das músicas X Anos #
data_source_2 = read_data.marciano_plot2_data("visualizacoes/data/spotify_youtube_year.csv")  # Função para gerar os dados do plot 2

plot_2 = figure(width=600, height = 600, x_range = [2006, 2021], tools = "box_zoom, pan, reset, save, wheel_zoom") # Criando a figura do gráfico 2
 
plot_2.line(x = "release_date", y = "Duration_s", source = data_source_2, line_width=2) # Criando o line plot com os dados do ColumnDataSource

plot_2.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
plot_2.background_fill_alpha = 0.1 # Definindo transparência do fundo do gráfico

# Definindo o Título
plot_2.title.text = "Music Duration in Time"
plot_2.title.text_color = "Black"
plot_2.title.text_font = "Arial Black"
plot_2.title.text_font_size = "30px"
plot_2.title.align = "center"

# Legenda do eixo X
plot_2.xaxis.axis_label = "Years" # Definindo texto
plot_2.xaxis.axis_label_text_font = 'Arial Black' # Definindo fonte
plot_2.xaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
plot_2.xaxis.axis_label_text_color = 'Black' # Definindo cor da letra

# Legenda do eixo Y
plot_2.yaxis.axis_label = "Music Duration (segundos)" # Definindo texto
plot_2.yaxis.axis_label_text_font = 'Arial Black' # Definindo fonte
plot_2.yaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
plot_2.yaxis.axis_label_text_color = 'Black' # Definindo cor da letra

tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre pontos da linha
    ('Ano', '@release_date'),
    ('Duração Média', '@Duration_s'),
    ]
plot_2.add_tools(HoverTool(tooltips=tooltips))

select_years = figure(title = "Arraste para selecionar os anos observados",  # Criando a figura da barra de rolagem para selecionar os anos
                    height = 130, width = 600, y_range = plot_2.y_range,     # Definindo o tamanho da figura, o range Y e tirando a toolbar
                    y_axis_type = None,
                    tools = "", toolbar_location = None)

select_years.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
select_years.background_fill_alpha = 0.1  # Definindo transparência do fundo do gráfico

select_years_tool = RangeTool(x_range = plot_2.x_range)   # Definindo o range da ferramenta de rolagem
select_years_tool.overlay.fill_color = "Blue"  # Cor da barra de rolagem
select_years_tool.overlay.fill_alpha = 0.15    # Transparência da barra de rolagem

select_years.line(x = "release_date", y = "Duration_s", source = data_source_2, line_color = "Blue") # Criando o plot na figura da barra de rolagem
select_years.ygrid.grid_line_color = None   # Tirando o grid Y da barra de rolagem
select_years.add_tools(select_years_tool)   # Adicionando a ferramenta para rolar o gráfico

plot_2 = column(plot_2,select_years)

########################################################################################################################

# Terceiro gráfico: Top 30 artistas #

data_source_3, lista_30_artistas = read_data.marciano_plot3_data("visualizacoes/data/spotify_youtube_year.csv")  # Função para gerar os dados do plot 3

plot_3 = figure(y_range=lista_30_artistas, height=600, width=600, tools = "") # Criando a figura do gráfico 3

plot_3.hbar(y='Artist', right='Stream', height=0.8, source=data_source_3) # Criando o horizontal bar plot com os dados co ColumnDataSource

plot_3.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
plot_3.background_fill_alpha = 0.1 # Definindo transparência do fundo do gráfico

# Definindo o Título
plot_3.title.text = "Top 30 Artists Streams"
plot_3.title.text_color = "Black"
plot_3.title.text_font = "Arial Black"
plot_3.title.text_font_size = "30px"
plot_3.title.align = "center"

# Labels do eixo Y
plot_3.yaxis.major_label_text_color = "Black" # Definindo a cor do nome dos artistas
plot_3.yaxis.major_label_text_font = "Arial Black" # Definindo a fonte do nome dos artistas

# Eixo X
plot_3.xgrid.grid_line_color = None # Tirando o grid do eixo X
plot_3.xaxis.axis_line_alpha=0 # Tirando a linha do eixo X
plot_3.xaxis.minor_tick_line_alpha = 0 # Tirando as marcações pequenas do eixo X 
plot_3.xaxis.major_tick_line_alpha = 0 # Tirando as marcações maiores do eixo X
plot_3.xaxis.major_label_text_alpha = 0 # Tirando as labels do eixo X

# Eixo Y
plot_3.yaxis.axis_label = "Artists" # Definindo texto
plot_3.yaxis.axis_label_text_font = 'Arial Black' # Definindo fonte
plot_3.yaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
plot_3.yaxis.axis_label_text_color = 'Black' # Definindo cor da letra
plot_3.ygrid.grid_line_color = None # Tirando o grid do eixo Y

tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre as barras
    ('Nº Médio de Streams', '@Stream'),
    ]
plot_3.add_tools(HoverTool(tooltips=tooltips))

labels = LabelSet(x="Stream", y="Artist", text="stream_label", x_offset=-50, y_offset=-7, source=data_source_3,  # Adicionando legenda nas barras
                  level = "glyph", text_font_size="10pt", text_font = "Arial Black", text_font_style = "bold", text_color = "#DEF8F9")
plot_3.add_layout(labels)

############################################################################################

layout = column(row(plot_1, plot_2), plot_3) # Definindo layout

show(layout)