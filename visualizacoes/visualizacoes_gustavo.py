# Arquivo para os códigos das  visualizacoes
import pandas as pd
import numpy as np

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show

df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv')

df_views_por_artista = df.groupby('Artist')['Views'].sum().sort_values(ascending=False)

df_views_por_track = df.groupby('Track')['Views'].sum().sort_values(ascending=False)

df_100_mais_vistos = df_views_por_track.head(100)

df.rename(columns={'release_date': 'year'}, inplace=True)

df['year'] = pd.to_datetime(df['year'], format='%Y')

to_cds = df.groupby('year').count()

source = ColumnDataSource(to_cds)

p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(df['year'].min(), df['year'].max()))

p.line('year', 'Key', source=source)
p.yaxis.axis_label = 'Contagem'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('year', 'Key', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)

show(column(p, select))

