# Arquivo para os códigos das  visualizacoes

from read_data import csv_to_columndatasource
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.annotations import Span, BoxAnnotation


output_file("vis_marciano.html")

# scatter plot speechiness X (outra variável) rascunho 

data = csv_to_columndatasource("visualizacoes/data/spotify_youtube.csv")

plot_1 = figure()

data["size"] = data["Stream"] / 100000

plot_1.circle(x = "Speechiness", y = "Loudness", source = data, color = "DeepPink", alpha = 0.8, size = "size")

box_annotation = BoxAnnotation(left=0, right=0.3333, fill_color = "DeepPink", fill_alpha = 0.3)
plot_1.add_layout(box_annotation)

show(plot_1)

# ranking de artistas rascunho
plot_2 = figure()

#plot_2.

# (variável) X tempo
