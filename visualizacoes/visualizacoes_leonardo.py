# Importações das funções dos módulos

from read_data import csv_to_columndatasource
from bokeh.plotting import figure
from bokeh.io import output_file, save, show
import pandas as pd

# Teste

df = pd.read_csv('visualizacoes/data/spotify_youtube_year.csv')

plot_1 = figure()

plot_1.circle(x = "Energy", y = "Danceability", source = df)

show(plot_1)