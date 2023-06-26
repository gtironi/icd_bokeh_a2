'''Módulo de leitura do arquivo .csv com os dados

Este módulo contém funções para gerar objetos ColumnDataSource a partir de um arquivo .csv

Funcionalidades:
- csv_to_columndatasouce: gera um objeto ColumnDataSource a partir de um arquivo .csv
'''

# Importando as bibliotecas usadas nesse modulo
import pandas as pd
from bokeh.models import ColumnDataSource

def csv_to_columndatasource(path, colunas = []):
    '''Gera um objeto ColumnDataSource a partir de um arquivo .csv

    Lê o arquivo .csv, armazenando o conteudo dele em um dataframe do 
    pandas, então seleciona as colunas desejadas (todas por padrão) e 
    gera um objeto ColumnDataSource corespondente. O objeto gerado pode
    ser usado para elaboração das visualizações com a biblioteca bokeh.

    Parametros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        colunas : list
            Deve conter uma lista com o nome das colunas que serão colocadas
            no ColumnDataSource. Por padrão, adiciona todas as colunas.
                Ex: ["col1", "col2", "col4"]

        Retorna
        -------
        data_source
            Retorna o ColumnDataSource gerado a partir dos paramentros fornecidos.

        Examples
        --------
        >>> csv_to_columndatasource("data/sleep_efficiency.csv", ['Exercise frequency', 'Deep sleep percentage'])
    '''

    df = pd.read_csv(path) 
    if colunas != []:
        df = df.loc[:, colunas]
    
    data_source = ColumnDataSource(df)

    return data_source
