# Arquivo para os códigos das  visualizacoes
import pandas as pd
import numpy as np

from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, RangeTool, OpenURL, TapTool, CustomJS
from bokeh.plotting import figure, show

df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv')

df.rename(columns={'release_date': 'year'}, inplace=True)

df['year'] = pd.to_datetime(df['year'], format='%Y')

to_cds = df.groupby('year').count()

source = ColumnDataSource(to_cds)

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

df_100_mais_vistos_completo['Views'] = df_100_mais_vistos_completo['Views']/1000000

source = ColumnDataSource(df_100_mais_vistos_completo)

p3 = figure(height=480, width=640, toolbar_location='right',
            x_axis_location="below", background_fill_color="#efefef")

p3.circle('Liveness', 'Views', size=6, source=source)
p3.yaxis.axis_label = 'Visualizações (em milhões)'
p3.xaxis.axis_label = 'Liveness'

select_layout = column(row(column(p, select), p2), p3)

show(select_layout)

