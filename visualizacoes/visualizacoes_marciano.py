# Arquivo para os códigos das  visualizacoes

import pandas as pd
from read_data import column_as_size
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.annotations import BoxAnnotation

from bokeh.models import HoverTool, ColumnDataSource


output_file("vis_marciano.html")


# scatter plot speechiness X (outra variável) rascunho 

data = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv")

#data = column_as_size(data, "Stream", 70000000)

color = []

for each_float in data["Liveness"]:
    if each_float >= 0.8:
        color.append("Red")
    else:
        color.append("Gray")
    # if each_float >= 2/3:
    #     color.append("Red")
    # elif each_float >= 1/3:
    #     color.append("Blue")
    # else:
    #     color.append("Green")

data["color"] = color

plot_1 = figure(width=600, height = 600, title = "Circle Glyphs")

data_source_1 = ColumnDataSource(data)

plot_1.circle(x = "Liveness", y = "Energy", source = data_source_1, color = "color", alpha = 0.4, size = 8)

# box_annotation_1 = BoxAnnotation(bottom=0, top=1/3, fill_color = "Green", fill_alpha = 0.2)
# plot_1.add_layout(box_annotation_1)
# box_annotation_2 = BoxAnnotation(bottom=1/3, top=2/3, fill_color = "Blue", fill_alpha = 0.2)
# plot_1.add_layout(box_annotation_2)
# box_annotation_3 = BoxAnnotation(bottom=2/3, top=1, fill_color = "Red", fill_alpha = 0.2)
# plot_1.add_layout(box_annotation_3)
box_annotation_4 = BoxAnnotation(left=0.8, right=1, fill_color = "Red", fill_alpha = 0.2)
plot_1.add_layout(box_annotation_4)

tooltips = [
    ('Música', '@Track'),
    ('Artista', '@Artist'),
    ('Álbum', '@Album'),
    ('Streams', '@Stream')]

plot_1.add_tools(HoverTool(tooltips=tooltips))


# show(plot_1)

######################################################################################
# (variável) X tempo
plot_2 = figure()

data = pd.DataFrame(data.groupby(["release_date"])["Tempo"].mean())

data_source_2 = ColumnDataSource(data)

plot_2.line(x = "release_date", y = "Tempo", source = data_source_2)

show(plot_2)
######################################################################################
# ranking de artistas rascunho
