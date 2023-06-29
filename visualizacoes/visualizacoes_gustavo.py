# Arquivo para os códigos das  visualizacoes
import pandas as pd
import numpy as np
from temporary import figure_generator_gustavo

from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, RangeTool, Whisker, PanTool
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap



df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv') #lê o csv

df.rename(columns={'release_date': 'year'}, inplace=True) #Renomeia a coluna, para melhor legibilidade do código.

df['year'] = pd.to_datetime(df['year'], format='%Y') #Transforma a o interio yyyy (ex: 2020), em datetime.

df.drop_duplicates('Track', inplace= True) #Retira as musicas duplicadas

df_by_year = df.groupby('year').count() #Agrupa por ano e conta a quantidade de musicas em cada ano

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

####

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

####

df = df[['official_video', 'popularity']].rename(columns= {'popularity': 'Likes'})

df['official_video'] = df['official_video'].astype(str)

kinds = ['True', 'False']

qs = df.groupby('official_video').Likes.quantile([0.25, 0.5, 0.75])
qs = qs.unstack().reset_index()
qs.columns = ['official_video', "q1", "q2", "q3"]
df = pd.merge(df, qs, on='official_video', how="left")

iqr = df.q3 - df.q1
df["upper"] = df.q3 + 1.5*iqr
df["lower"] = df.q1 - 1.5*iqr

source = ColumnDataSource(df)

p4 = figure(x_range=kinds, tools="", toolbar_location=None,
           background_fill_color="#efefef", y_axis_label="Popularidade",
           y_range = (df['Likes'].min(), df['Likes'].max()))

whisker = Whisker(base='official_video', upper="upper", lower="lower", source=source)
whisker.upper_head.size = whisker.lower_head.size = 20
p4.add_layout(whisker)

cmap = factor_cmap('official_video', "TolRainbow7", kinds)
p4.vbar('official_video', 0.7, "q2", "q3", source=source, color=cmap, line_color="black")
p4.vbar('official_video', 0.7, "q1", "q2", source=source, color=cmap, line_color="black")

outliers = df[~df.Likes.between(df.lower, df.upper)]
p4.scatter('official_video', "Likes", source=outliers, size=6, color="black", alpha=0.3)

p4.xgrid.grid_line_color = None
p4.axis.major_label_text_font_size="14px"
p4.axis.axis_label_text_font_size="12px"

select_layout = column(p1, row(p2, p4))

show(select_layout)