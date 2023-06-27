'''Módulo para juntar duas bases de dados do kaggle

Não possui funções definidas, pois só é executado uma vez.

Basicamente, ele lê as bases de dados 'spotify_youtube.csv' e 'tracks.csv', altera o formato da data, 
para deixar apeans o ano e trata os dados para dar um merge nos dataframes.
Com isso, a coluna 'popularity' e 'release_date' são adicionadas a base de dados inicial (spotify_youtube.csv)
e o resultado é salvo no arquivo 'spotify_youtube_year.csv'.
'''

import pandas as pd

spoty_youtube = pd.read_csv("visualizacoes/data/spotify_youtube.csv") #lê o arquivo spotify_youtube.csv

spoty_year = pd.read_csv("visualizacoes/data/tracks.csv", usecols = ['release_date','name', 'popularity'] , dtype = {'name': str, 'popularity': float}) #lê o arquivo tracks.csv

spoty_year['release_date'] = pd.to_datetime(spoty_year['release_date'], format = '%Y-%m-%d').dt.year #transforma a data em datetime64 e extrai apenas o ano com o 'dt.year'

spoty_year.rename(columns={'name': 'Track'}, inplace=True) #renomeia a coluna, para o nome coincidir nas bases

spoty_year = spoty_year.drop_duplicates("Track").dropna() #remove valores duplicados e NA's

new_data = pd.merge(spoty_youtube, spoty_year, on="Track") #junta os dataframes por meio do 'merge', tendo como referência a coluna 'Track'

new_data.drop(new_data.columns[new_data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True) #remove a coluna gerada pelos index dos .csv lidos

new_data.to_csv('visualizacoes/data/spotify_youtube_year.csv', index=False) #salva a nova base no arquivo spotify_youtube_year.csv, dentro da pasta 'data'