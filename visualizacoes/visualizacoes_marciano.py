# Arquivo para os códigos das  visualizacoes

# Importando os módulos utilizados
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models.annotations import BoxAnnotation
from bokeh.models import HoverTool, Label, RangeTool, LabelSet
from bokeh.layouts import column, row
import read_data


########################################################################################################################
# Primeiro gráfico: Scatter plot Liveness X Energy #

def plot_1_marciano(data_source):

    plot_1 = figure(width=600, height = 600, tools = "box_zoom, pan, reset, save, wheel_zoom") # Criando a figura do gráfico 2

    plot_1.circle(x = "Liveness", y = "Energy", source = data_source, color = "color", alpha = 0.4, size = 8) #Criando scatter plot com os dados do data_source

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

    box_annotation_1 = BoxAnnotation(left=0.8, right=1, fill_color = "Blue", fill_alpha = 0.15) # Criando retângulo e adicionando ao gráfico
    plot_1.add_layout(box_annotation_1) 

    annotation_1 = Label(x=0.775, y=0.1, text="Músicas ao vivo", text_font_size="10pt",text_font = "Arial Black"   # Criando uma anotação do gráfico
                    , text_color="Blue", background_fill_alpha=0.0)                                 
    plot_1.add_layout(annotation_1)                                                                            # Adicionando anotação por cima do gráfico

    tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre os glifos
        ('Música', '@Track'),
        ('Artista', '@Artist'),
        ('Álbum', '@Album'),
        ('Streams', '@Stream')]
    plot_1.add_tools(HoverTool(tooltips=tooltips))

    return(plot_1)

source_1 = read_data.columndatasource_plot1_marciano("visualizacoes/data/spotify_youtube_year.csv")
plot_1 = plot_1_marciano(source_1) # Criando efetivamente o plot 1

########################################################################################################################
# Segundo gráfico: Duração das músicas X Anos #

def plot_2_marciano(data_source, mean_duration):

    plot_2 = figure(width=600, height = 600, x_range = [2006, 2021], tools = "box_zoom, pan, reset, save, wheel_zoom") # Criando a figura do gráfico 2
    
    plot_2.line(x = "release_date", y = "Duration_s", source = data_source, line_width=2) # Criando o line plot com os dados do ColumnDataSource

    plot_2.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
    plot_2.background_fill_alpha = 0.1 # Definindo transparência do fundo do gráfico

    # Definindo o Título
    plot_2.title.text = "Duração da música pelo tempo"
    plot_2.title.text_color = "Black"
    plot_2.title.text_font = "Arial Black"
    plot_2.title.text_font_size = "30px"
    plot_2.title.align = "center"

    # Legenda do eixo X
    plot_2.xaxis.axis_label = "Anos" # Definindo texto
    plot_2.xaxis.axis_label_text_font = 'Arial Black' # Definindo fonte
    plot_2.xaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
    plot_2.xaxis.axis_label_text_color = 'Black' # Definindo cor da letra

    # Legenda do eixo Y
    plot_2.yaxis.axis_label = "Duração da música (segundos)" # Definindo texto
    plot_2.yaxis.axis_label_text_font = 'Arial Black' # Definindo fonte
    plot_2.yaxis.axis_label_text_font_size = '18px' # Definindo tamanho da letra
    plot_2.yaxis.axis_label_text_color = 'Black' # Definindo cor da letra

    tooltips = [                       # Definindo as informações das músicas que aparecerão ao passar o mouse sobre pontos da linha
        ('Ano', '@release_date'),
        ('Duração Média', '@Duration_s'),
        ]
    plot_2.add_tools(HoverTool(tooltips=tooltips))

    box_annotation_2 = BoxAnnotation(left=2018.5, right=2021.5,top = 212, bottom = 196, fill_color = "Red", fill_alpha = 0.15) # Criando retângulo e adicionando ao gráfico
    plot_2.add_layout(box_annotation_2)

    plot_2.line(x="release_date", y= mean_duration, source= data_source, line_width=3, line_color = "Red", legend_label="Duração média total")

    annotation_2 = Label(x=2014, y=198, text="Decaimento da duração\n média das músicas\n nesses 3 anos", text_font_size="10pt",text_font = "Arial Black"   # Criando uma anotação do gráfico
                    , text_color="Red", background_fill_alpha=0.0)                                 
    plot_2.add_layout(annotation_2)  

    select_years = figure(title = "Arraste para selecionar os anos observados",  # Criando a figura da barra de rolagem para selecionar os anos
                        height = 130, width = 600, y_range = plot_2.y_range,     # Definindo o tamanho da figura, o range Y e tirando a toolbar
                        y_axis_type = None,
                        tools = "", toolbar_location = None)

    select_years.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
    select_years.background_fill_alpha = 0.1  # Definindo transparência do fundo do gráfico

    select_years_tool = RangeTool(x_range = plot_2.x_range)   # Definindo o range da ferramenta de rolagem
    select_years_tool.overlay.fill_color = "Blue"  # Cor da barra de rolagem
    select_years_tool.overlay.fill_alpha = 0.15    # Transparência da barra de rolagem

    select_years.line(x = "release_date", y = "Duration_s", source = data_source, line_color = "Blue") # Criando o plot na figura da barra de rolagem
    select_years.ygrid.grid_line_color = None   # Tirando o grid Y da barra de rolagem
    select_years.add_tools(select_years_tool)   # Adicionando a ferramenta para rolar o gráfico

    plot_2 = column(plot_2,select_years)

    return(plot_2)

source_2 = read_data.columndatasource_plot2_marciano("visualizacoes/data/spotify_youtube_year.csv")[0]
mean_duration = read_data.columndatasource_plot2_marciano("visualizacoes/data/spotify_youtube_year.csv")[1]
plot_2 = plot_2_marciano(source_2, mean_duration) # Criando efetivamente o plot 2

########################################################################################################################

# Terceiro gráfico: Top 30 artistas #

data_source_3, lista_30_artistas = read_data.columndatasource_plot3_marciano("visualizacoes/data/spotify_youtube_year.csv")  # Função para gerar os dados do plot 3
def plot_3_marciano(data_source, top_30_list):

    plot_3 = figure(y_range=top_30_list, height=600, width=600, tools = "") # Criando a figura do gráfico 3

    plot_3.hbar(y='Artist', right='Stream', height=0.8, source=data_source_3) # Criando o horizontal bar plot com os dados co ColumnDataSource

    plot_3.background_fill_color = "Yellow" # Definindo cor de fundo do gráfico
    plot_3.background_fill_alpha = 0.1 # Definindo transparência do fundo do gráfico

    # Definindo o Título
    plot_3.title.text = "Top 30 Artistas mais ouvidos"
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
    plot_3.yaxis.axis_label = "Artistas" # Definindo texto
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

    return(plot_3)


source_3 = read_data.columndatasource_plot3_marciano("visualizacoes/data/spotify_youtube_year.csv")[0]
top_30_list = read_data.columndatasource_plot3_marciano("visualizacoes/data/spotify_youtube_year.csv")[1]
plot_3 = plot_3_marciano(source_3, top_30_list)   # Criando efetivamente o plot 3
############################################################################################

layout = column(row(plot_1, plot_2), plot_3) # Definindo layout

show(layout)