# Arquivo para os códigos das  visualizacoes
import numpy as np

from . import plot_style
from . import generic_plot
from . import read_data 

from bokeh.layouts import column, row
from bokeh.models import RangeTool, Div
from bokeh.plotting import figure

# Plot 1 (lineplot)

def plot_1_gustavo(datapath):

    source = read_data.columndatasource_plot1_gustavo(datapath) #Chama a função que retorna o ColumnDataSource
    
    plot_1 = plot_style.figure_generator_gustavo(figure(height=350, width=890, tools="xpan", toolbar_location=None, 
                                             x_axis_type="datetime", x_axis_location="above", 
                                             x_range=(np.datetime64('1970-01-01'), np.datetime64('2020-01-01')))) #Chama a função de estilo, criando a figura que será usada para fazer o gráfico

    #Altera as linhas de grade do plot
    plot_1.xgrid.grid_line_color = 'gray'
    plot_1.xgrid.grid_line_alpha = 0.1

    #Coloca texto nos eixos e título
    plot_1.xaxis.axis_label = 'Anos'
    plot_1.yaxis.axis_label = 'Músicas lançadas'
    plot_1.title.text = 'Quantidade de músicas lançadas por ano'

    #Gera o gráfico de linhas, usando o metodo line()
    plot_1.line('year', 'Key', source=source)

    barra_de_rolagem = plot_style.figure_generator_gustavo(figure(height=230, width=890, y_range = plot_1.y_range,
                                                       x_axis_type="datetime", y_axis_type=None, tools="", toolbar_location=None)) #Chama a função de estilo, criando a figura que será usada para a barra de rolagem
    
    #Altera caracteristicas visuais da figura barra de rolagem
    barra_de_rolagem.title.text_font_size = '16px'
    barra_de_rolagem.xgrid.grid_line_color = 'gray'
    barra_de_rolagem.xgrid.grid_line_alpha = 0.1
    barra_de_rolagem.title.text = 'Arraste para mover o gráfico'
    barra_de_rolagem.min_border_bottom = 100

    #Usa a ferramenta RangeTool() para transforar a figura e uma barra de rolagem, que está linkada com o plot principal
    range_tool = RangeTool(x_range=plot_1.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    #Coloca o plot principal na barra de rolagem, fazendo ele parecer ao fundo
    barra_de_rolagem.line('year', 'Key', source=source)
    barra_de_rolagem.add_tools(range_tool)

    return column(plot_1, barra_de_rolagem) #Junta o plot principal e a barra de rolagem, fazendo deles uma coisa só

# Plot 2 (scatterplot)

def plot_2_gustavo(datapath, column):

    datasource = read_data.columndatasource_plot2_gustavo(datapath) #Chama a função que retorna o ColumnDataSource

    tooltips = [
    ("Nome", "@Track"),
    ("Artista", "@Artist"),
    ("Views", "@Views"),
    ("URL", "@Url_youtube"),] #Defini quais tooltips mostrar, e de qual coluna extrair o valor

    plot_2 = plot_style.figure_generator_gustavo(figure(height=480, width=690, toolbar_location=None,
                                             tools="hover", tooltips=tooltips)) #Chama a função de estilo, criando a figura que será usada para fazer o gráfico

    #Gera o gráfico de dispersão, usando o metodo circle()
    plot_2.circle(column, 'Views', size=8, source=datasource)

    #Coloca texto nos eixos e título
    plot_2.yaxis.axis_label = 'Visualizações (em milhões)'
    plot_2.xaxis.axis_label = column.capitalize()
    plot_2.title.text = f'{column.capitalize()} vs Visualizações'

    return plot_2 #Retorna a figura

# Plot 3 (boxplot)

def plot_3_gustavo(datapath):

    dataframe = read_data.columndatasource_plot3_gustavo(datapath) #Chama a função que retorna o dataframe

    plot_3 = generic_plot.boxplot(dataframe, 'official_video', 'popularity') #Chama a função que gera o boxplot, usando o dataframe anteriror

    #Coloca texto nos eixos e título
    plot_3.yaxis.axis_label = 'Popularidade'
    plot_3.title.text = 'Boxplot - Oficial Vídeo'

    return plot_3 #Retorna a figura

def cria_layout_gustavo(datapath):

    plot_1 = plot_1_gustavo(datapath) #Chama a função do plot 1, salvando a figura resultante na variavel plot_1

    plot_2 = plot_2_gustavo(datapath, 'Acousticness') #Chama a função do plot 2, salvando a figura resultante na variavel plot_2

    plot_3 = plot_3_gustavo(datapath) #Chama a função do plot 3, salvando a figura resultante na variavel plot_3

    text1 = Div(text=""" <h2>Gráfico de linha</h2>
    <p>Ao lado, foi plotado um gráfico de linha, o qual demonstra a quantidade de músicas, no dataset, lançadas por ano.<br>
    Para sua execução, o dataset foi agrupado por ano, então foi contado a quantidade de ocorrências e utilizando o 
    método <b>line()</b> para fazer o plot principal.<br>
    Ainda, foi adicionado uma barra de rolagem abaixo do gráfico, que permite rolar o gráfico. Essa barra usa a ferramenta
    <b>RangeTool</b> e a conexão entre o plot e barra de rolagem, para gerar o efeito apresentado.<p>
    """, 
    style = {'text-align': 'center', 'font-size': '16px'}, width=430, align = 'center')

    text2 = Div(text=""" <h2>Gráfico de dispersão</h2>
    <p>Acima, foi plotado um gráfico de dispersão, dessa vez, considerando apenas as <b>100 músicas mais visualizadas</b><br>
    no YouTube. Esse gráfico demonstra uma referência acústica (Acousticness) vs a quantidade de visualizações de cada música. 
    Além disso, ao colocar o mouse em cima de um dos pontos, é possível ver o <b>nome da música</b>, o <b>artista</b>, a 
    <b>quantidade de visualizações</b> e a <b>URL</b>, que leva à página da música em questão no YouTube.<br>
    Para sua execução, o dataset foi filtrado, sobrando apenas as 100 músicas com mais views, e então utilizado o método 
    <b>circle()</b> para fazer o plot.<p>
    """,
    style = {'text-align': 'center', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))

    text3 = Div(text=""" <h2>Gráfico Boxplot</h2>
    <p>Acima, foi plotado um <b>boxplot</b>, da popularidade das músicas, conforme a existência de um videoclipe.<br>
    Esse gráfico demonstra a distribuição dos valores em cada categoria, bem como identifica os <b>outliers</b>. 
    Para sua execução, foi definida uma função - baseada na documentação do bokeh - que monta cada parte do boxplot
    individualmente. Essa função, calcula todos os valores necessários, e plota cada elemento do boxplot a partir disso.<br>
    Superficialmente, observando o boxplot, podemos dizer que há um indicativo de maior popularidade em
    músicas com videoclipe.
    """,
    style = {'text-align': 'center', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))
    
    layout_final = column(row(plot_1, text1), row(column(plot_2, text2), column(plot_3, text3))) #Define o layout final, juntando os textos e os gráficos

    return layout_final #Retorna o layout final