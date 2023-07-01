
from bokeh.models import Select, Div
from bokeh.layouts import column, row
from bokeh.plotting import curdoc
# from visualizacoes.visualizacoes_marciano import cria_layout_marciano
# from visualizacoes.visualizacoes_gustavo import cria_layout_gustavo
from visualizacoes import gera_layout_sillas
# from visualizacoes.visualizacoes_leonardo import gera_layout_leonardo

# path = "visualizacoes/data/spotify_youtube_year.csv"



layout_sillas = gera_layout_sillas("visualizacoes/data/spotify_youtube_year.csv")
# page = gera_bokeh_server("visualizacoes/data/spotify_youtube_year.csv")

curdoc().add_root(layout_sillas)

