'''Módulo para juntar duas bases de dados do kaggle

Não possui funções definidas, pois só é executado uma vez.

Basicamente, ele lê as bases de dados 'spotify_youtube.csv' e 'tracks.csv', altera o formato da data, 
para deixar apeans o ano e trata os dados para dar um merge nos dataframes, baseado no nome da música
e no artista que a compôs.
Com isso, a coluna 'popularity' e 'release_date' são adicionadas a base de dados inicial (spotify_youtube.csv)
e o resultado é salvo no arquivo 'spotify_youtube_year.csv'.
'''

import pandas as pd

spoty_youtube = pd.read_csv("visualizacoes/data/spotify_youtube.csv") #lê o arquivo spotify_youtube.csv

spoty_year = pd.read_csv("visualizacoes/data/tracks.csv", usecols = ['name', "artist", 'popularity', 'release_date'],
                         dtype = {'name': str, "artist": str, 'popularity': float}) #lê o arquivo tracks.csv

spoty_year['release_date'] = pd.to_datetime(spoty_year['release_date'], format = 'ISO8601').dt.year #transforma a data em datetime64 e extrai apenas o ano com o 'dt.year'

spoty_year["track_artist"] = spoty_year["name"] + spoty_year["artist"] #gera a coluna que une o nome da música com o nome do compositor no arquivo tracks.csv

spoty_year = spoty_year.sort_values(by = ["release_date", "popularity"], ascending = [True, False]).drop_duplicates("track_artist") #ordena para obter o ano de lançamento mais antigo com a maior popularidade e remove valores duplicados

spoty_youtube["track_artist"] = spoty_youtube["Track"] + spoty_youtube["Artist"] #gera a coluna que une o nome da música com o nome do compositor no arquivo spotify_youtube.csv

new_data = pd.merge(spoty_youtube, spoty_year, on="track_artist") #junta os dataframes por meio do 'merge', tendo como referência a coluna 'track_artist'

new_data = new_data.drop(["track_artist", "name", "artist"], axis = 1) #exclui as colunas desnecessárias que já estão na base original

new_data.drop(new_data.columns[new_data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True) #remove a coluna gerada pelos index dos .csv lidos

new_data.to_csv('visualizacoes/data/spotify_youtube_year.csv', index=False) #salva a nova base no arquivo spotify_youtube_year.csv, dentro da pasta 'data'