# Arquivo para os códigos das  visualizacoes
import pandas as pd
import numpy as np
from temporary import figure_generator_gustavo
from generic_plot import boxplot

from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, RangeTool, Whisker, PanTool
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv') #lê o csv

# Plot 1 (lineplot)

df.rename(columns={'release_date': 'year'}, inplace=True) #renomeia a coluna, para melhor legibilidade do código.

df['year'] = pd.to_datetime(df['year'], format='%Y') #transforma a o interio yyyy (ex: 2020), em datetime.

df.drop_duplicates('Track', inplace= True) #retira as musicas duplicadas

df_by_year = df.groupby('year').count() #agrupa por ano e conta a quantidade de musicas em cada ano

source = ColumnDataSource(df_by_year) #transforma o .csv em ColumnDataSource

def plot_1_gustavo(datasource):
    plot_1 = figure_generator_gustavo(figure(height=350, width=640, tools="xpan", toolbar_location=None, 
                                             x_axis_type="datetime", x_axis_location="above", 
                                             x_range=(np.datetime64('1970-01-01'), np.datetime64('2020-01-01'))))

    plot_1.xgrid.grid_line_color = 'gray'
    plot_1.xgrid.grid_line_alpha = 0.1

    plot_1.xaxis.axis_label = 'Anos'
    plot_1.yaxis.axis_label = 'Músicas lançadas'
    plot_1.title.text = 'Quantidade de músicas lançadas por ano'

    plot_1.line('year', 'Key', source=source)

    barra_de_rolagem = figure_generator_gustavo(figure(height=130, width=640, y_range = plot_1.y_range,
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

df_views_por_track = df.sort_values(by = 'Views', ascending=False).drop_duplicates('Track')

df_100_mais_vistos_completo = (df_views_por_track).head(100)

df_100_mais_vistos_completo.loc[:, 'Views'] = df_100_mais_vistos_completo['Views']/1000000

source1 = ColumnDataSource(df_100_mais_vistos_completo)

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

df = df[['official_video', 'popularity']].rename(columns= {'popularity': 'Likes'})

df['official_video'] = df['official_video'].astype(str)

def plot_3_gustavo(dataframe):

    plot_3 = boxplot(dataframe, 'official_video', 'Likes')

    plot_3.yaxis.axis_label = 'Popularidade'

    return plot_3

p3 = plot_3_gustavo(df)

select_layout = column(p1, row(p2, p3))

show(select_layout)