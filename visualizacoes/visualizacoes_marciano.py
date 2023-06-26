# Arquivo para os códigos das  visualizacoes

from read_data import csv_to_columndatasource
from bokeh.plotting import figure
from bokeh.io import output_file, save, show

output_file("vis_marciano.html")

data = csv_to_columndatasource("visualizacoes/data/spotify_youtube.csv")

plot = figure()

plot.circle(x = "Duration_ms", y = "Stream", source = data)

show(plot)

