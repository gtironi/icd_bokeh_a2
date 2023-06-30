# Arquivo para os códigos das  visualizacoes
import pandas as pd
import numpy as np

from .plot_style import figure_generator_gustavo
from .generic_plot import boxplot
from .read_data import columndatasource_plot1_gustavo, columndatasource_plot2_gustavo, columndatasource_plot3_gustavo

from bokeh.layouts import column, row
from bokeh.models import RangeTool, Div
from bokeh.plotting import figure, show

df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv') #lê o csv

# Plot 1 (lineplot)

source = columndatasource_plot1_gustavo('visualizacoes/data/spotify_youtube_year.csv')

def plot_1_gustavo(datasource):
    plot_1 = figure_generator_gustavo(figure(height=350, width=840, tools="xpan", toolbar_location=None, 
                                             x_axis_type="datetime", x_axis_location="above", 
                                             x_range=(np.datetime64('1970-01-01'), np.datetime64('2020-01-01'))))

    plot_1.xgrid.grid_line_color = 'gray'
    plot_1.xgrid.grid_line_alpha = 0.1

    plot_1.xaxis.axis_label = 'Anos'
    plot_1.yaxis.axis_label = 'Músicas lançadas'
    plot_1.title.text = 'Quantidade de músicas lançadas por ano'

    plot_1.line('year', 'Key', source=source)

    barra_de_rolagem = figure_generator_gustavo(figure(height=130, width=840, y_range = plot_1.y_range,
                                                       x_axis_type="datetime", y_axis_type=None, tools="", toolbar_location=None))
    
    barra_de_rolagem.title.text_font_size = '16px'
    barra_de_rolagem.xgrid.grid_line_color = 'gray'
    barra_de_rolagem.xgrid.grid_line_alpha = 0.1
    barra_de_rolagem.title.text = 'Arraste para mover o gráfico'

    range_tool = RangeTool(x_range=plot_1.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    barra_de_rolagem.line('year', 'Key', source=source)
    barra_de_rolagem.add_tools(range_tool)

    return column(plot_1, barra_de_rolagem)

p1 = plot_1_gustavo(source)

# Plot 2 (scatterplot)

source1 = columndatasource_plot2_gustavo('visualizacoes/data/spotify_youtube_year.csv')

def plot_2_gustavo(datasource, column):

    tooltips = [
    ("Nome", "@Track"),
    ("Artista", "@Artist"),
    ("Views", "@Views"),
    ("URL", "@Url_youtube"),]

    plot_2 = figure_generator_gustavo(figure(height=480, width=640, toolbar_location=None,
                                             tools="hover", tooltips=tooltips))

    plot_2.circle(column, 'Views', size=8, source=datasource)
    plot_2.yaxis.axis_label = 'Visualizações (em milhões)'
    plot_2.xaxis.axis_label = column.capitalize()
    plot_2.title.text = f'{column.capitalize()} vs Visualizações'

    return plot_2

p2 = plot_2_gustavo(source1, 'Acousticness')

# Plot 3 (boxplot)

df = columndatasource_plot3_gustavo('visualizacoes/data/spotify_youtube_year.csv')

def plot_3_gustavo(dataframe):

    plot_3 = boxplot(dataframe, 'official_video', 'popularity')

    plot_3.yaxis.axis_label = 'Popularidade'

    return plot_3

p3 = plot_3_gustavo(df)

text1 = Div(text=""" text 1

""")

text2 = Div(text=""" text 2

""")

text3 = Div(text=""" text 3

""")

select_layout = column(row(p1, text1), row(column(p2, text2), column(p2, text3)))

show(select_layout)