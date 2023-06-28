# Arquivo para os códigos das  visualizacoes

import pandas as pd
from read_data import column_as_size
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.annotations import BoxAnnotation
from bokeh.models import HoverTool, ColumnDataSource


output_file("vis_marciano.html")

'''
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
'''
######################################################################################
# (variável) X tempo

# plot_2 = figure()

# data = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv")

# data = pd.DataFrame(data.groupby(["release_date"])["Duration_ms"].mean())

# data_source_2 = ColumnDataSource(data)

# plot_2.line(x = "release_date", y = "duration_ms", source = data_source_2)

# show(plot_2)

######################################################################################

# ranking de artistas rascunho
data = pd.read_csv("visualizacoes/data/spotify_youtube_year.csv")

data = pd.DataFrame(data.groupby(["Artist"])["Stream"].mean().sort_values(ascending=False).head(30))

data_source_3 = ColumnDataSource(data=dict(Artist=data.index, Stream=data.values))

plot_3 = figure(y_range=data.index.tolist(), height=600, width=600, title="Top 30 Artistas Mais Ouvidos")

plot_3.hbar(y='Artist', right='Stream', height=0.8, source=data_source_3)

# plot_3.ygrid.grid_line_color = None
# plot_3.yaxis.axis_label = "Artistas"

show(plot_3)
