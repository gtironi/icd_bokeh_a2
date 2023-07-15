import html_estatico_final as html
from bokeh.io import show

html_final = html.gera_html('data/spotify_youtube_year.csv')

show(html_final)

