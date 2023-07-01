# Arquivo para os códigos das  visualizacoes

# Importando os módulos utilizados
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.models.annotations import BoxAnnotation
from bokeh.models import HoverTool, Label, RangeTool, LabelSet, Div
from bokeh.layouts import column, row
from . import read_data


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

    annotation_2 = Label(x=2014, y=198, text="Decaimento na duração\n média das músicas\n nesses 3 anos", text_font_size="10pt",text_font = "Arial Black"   # Criando uma anotação do gráfico
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
######################################################################################################################################
# Criando as explicações #
def cria_explicacoes_marciano():
    text_1 = Div(text = '''
    <h2>Scatter Plot Liveness X Energy</h2>
    A partir dos dados da base de dados, encontrada no Kaggle, sobre músicas do Spotify e YouTube, foi feita a visualização ao lado.
    O objetivo do gráfico é observar a possível correlação entre a "energia" da música e o fato dela ser ao vivo.
    A variável Energy é uma medida que representa o percentual de intensidade e atividade na música, já a Liveness mede a presença de audiencia na gravação.
    No site da base de dados no Kaggle foi dito que as músicas com valores de Liveness superiores a 0.8 são, muito provavelmente, gravações de músicas ao vivo. Com o intuito de observar se músicas ao vivo são mais "animadas", com maior percentual de "Energy", foi criado o gráfico de distribuição das duas variáveis. Como o objetivo é destacar as músicas 
    ao vivo, foi utilizada a cor e a anotação para dar ênfase. As músicas na área azul e com o glifo em azul, são gravações ao vivo. O usuário pode passar
    o mouse sobre os pontos para obter mais informações sobre as músicas, além de dar zoom e mexer navegar pelo gráfico.
    ''',
    style = {"text-align" : "center", "font-size" : "16px"}, width=430, align = "center", margin =(10,0,10,30))

    text_2 = Div(text = '''
    <h2>Duração das músicas X Anos</h2>
    <p>A partir dos dados da base de dados, encontrada no Kaggle, sobre músicas do Spotify e YouTube, foi feita a visualização.
    O objetivo do gráfico é observar com variou a duração das músicas pelo anos.
    Foram utilizadas as colunas Duration_ms, duração da música em milissegundos, e release_date, ano de lançamento da música, para fazer esse gráfico
    de linha. A variável Duration_ms foi transformada para segundos, dividindo os valores por 1000.
    Foi realizado um agrupamento das músicas por ano de lançamento, calculando a média de duração das músicas em cada ano.
    Foi realizado uma filtragem para utilizar somente os anos que possuiam um número considerável de músicas, que no caso foi mais que 90 músicas no ano,
    visto que haviam anos com somente uma música na base de dados. Por fim, foi feito o
    gráfico de linha para observar como a média de duração das músicas variou no tempo além de uma linha horizontal para fim de comparação
    que mostra a média geral de duração das músicas. Há uma barra para deslizar no tempo abaixo do gráfico.
    O usuário pode passar o mouse sobre a linha para obter mais informações em cada ano, além de dar zoom e mexer navegar pelo gráfico.</p>
    ''',
    style = {"text-align" : "center", "font-size" : "16px"}, width=430, align = "center", margin =(10,0,10,30))


    text_3 = Div(text = '''
    <h2>Top 30 artistas</h2>
    <p>A partir dos dados da base de dados, encontrada no Kaggle, sobre músicas do Spotify e YouTube, foi feita a visualização.
    O objetivo do gráfico é fazer um raking dos 30 artistas com maior média de streams da base de dados.
    Foram utilizadas as colunas Artist, artista da música, e Stream, número de reproduções da música, para fazer esse gráfico de barras.
    Foi realizado um agrupamento das músicas por artista, calculando a média de reproduções de cada artista.
    Por fim, foi realizado o gráfico de barras horizontais com os 30 maiores valores do data frame criado. O usuário pode passar
    o mouse sobre as barras para obter o número exato de streams, mas não pode navegar pelo gráfico, visto que é um ranking.</p>
    ''',
    style = {"text-align" : "center", "font-size" : "16px"}, width=430, align = "center", margin =(10,0,10,30))

    return [text_1, text_2, text_3]

#####################################################################################################################

def cria_layout_marciano(path):
    source_1 = read_data.columndatasource_plot1_marciano(path)
    plot_1 = plot_1_marciano(source_1)

    source_2 = read_data.columndatasource_plot2_marciano(path)[0]
    mean_duration = read_data.columndatasource_plot2_marciano(path)[1]
    plot_2 = plot_2_marciano(source_2, mean_duration)

    source_3 = read_data.columndatasource_plot3_marciano(path)[0]
    top_30_list = read_data.columndatasource_plot3_marciano(path)[1]
    plot_3 = plot_3_marciano(source_3, top_30_list)
    
    explicacoes = cria_explicacoes_marciano()

    text_1 = explicacoes[0]
    text_2 = explicacoes[1]
    text_3 = explicacoes[2]

    layout = column(row(plot_1, text_1), row(plot_2, text_2), row(plot_3, text_3)) # Definindo layout
    return layout

# layout = cria_layout_marciano()
# show(layout)