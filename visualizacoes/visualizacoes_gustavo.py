# Arquivo para os códigos das  visualizacoes
import pandas as pd
import numpy as np
from read_data import histogram_count

from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, RangeTool, Whisker
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap



df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv')

df.rename(columns={'release_date': 'year'}, inplace=True) #Renomeia a coluna, para melhor legibilidade do código.

df['year'] = pd.to_datetime(df['year'], format='%Y') #Transforma a o interio yyyy (ex: 2020), em datetime.

df.drop_duplicates('Track', inplace= True) #Retira as musicas duplicadas

df_by_year = df.groupby('year').count() #Agrupa por ano e conta a quantidade de musicas em cada ano

source = ColumnDataSource(df_by_year)

####

p = figure(height=350, width=640, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(np.datetime64('1970-01-01'), np.datetime64('2020-01-01')))

p.line('year', 'Key', source=source)
p.yaxis.axis_label = 'Contagem'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=640, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('year', 'Key', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

####

datetime = pd.to_datetime(df['Duration_ms'], unit='ms')

df['Duration_s'] = (datetime.dt.minute)*60 + datetime.dt.second

source = ColumnDataSource(df)

p2 = figure(height=480, width=640, tools="xpan", toolbar_location=None,
            x_axis_location="below", background_fill_color="#efefef",
            x_range=(0, 0.5), y_range=(0, 500))

p2.circle('Liveness', 'Duration_s', source=source)
p2.yaxis.axis_label = 'Duração em segundos'
p2.xaxis.axis_label = 'Speechiness'

####

df_views_por_track = df.sort_values(by = 'Views', ascending=False).drop_duplicates('Track')

df_100_mais_vistos_completo = (df_views_por_track).head(100)

df_100_mais_vistos_completo.loc[:, 'Views'] = df_100_mais_vistos_completo['Views']/1000000

source = ColumnDataSource(df_100_mais_vistos_completo)

p3 = figure(height=480, width=640, toolbar_location='right',
            x_axis_location="below", background_fill_color="#efefef")

p3.circle('Liveness', 'Views', size=6, source=source)
p3.yaxis.axis_label = 'Visualizações (em milhões)'
p3.xaxis.axis_label = 'Liveness'

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

select_layout = column(row(column(p, select), p2), row(p3, p4))

show(select_layout)