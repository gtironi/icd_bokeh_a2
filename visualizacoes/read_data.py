'''Módulo de leitura do arquivo .csv com os dados

Este módulo contém funções para gerar objetos ColumnDataSource a partir de um arquivo .csv

Funcionalidades:
- csv_to_columndatasouce: gera um objeto ColumnDataSource a partir de um arquivo .csv
'''

# Importando as bibliotecas usadas nesse modulo
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource

def csv_to_columndatasouce(path, colunas = []):
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
        >>> csv_to_columndatasouce("data/sleep_efficiency.csv", ['Exercise frequency', 'Deep sleep percentage'])
    '''

    df = pd.read_csv(path) 
    if colunas != []:
        df = df.loc[:, colunas]
    
    data_source = ColumnDataSource(df)

    return data_source


def csv_get_top(path, sort_column, duplicated_column = "", num = 10):
    """Gera um objeto ColumnDataSource a partir de um arquivo .csv

    Lê o arquivo .csv, o transforma em um data frame do pandas, e, a partir
    da coluna selecionada, orderna os valores em ordem decrescente e pega
    apenas a quantidade definida (por padrão os 10 primeiros), é possível
    também remover valores duplicados de alguma coluna.

    Parametros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        sort_colum : str
            Deve conter o nome de uma coluna da base de dados, a qual
            será feita a ordenação de valores.
            Deve conter exatamente um valor.
        duplicated_column : str, optional
            Deve conter o nome de uma coluna da base de dados, a qual
            possui valores duplicados
        num : int, optional
            Deve conter a quantidade de observações coletadas a partir
            da ordenação de valores (Por padrão 10).

        Retorna
        -------
        data_source
            Retorna o ColumnDataSource gerado a partir da ordenação do
            data frame.
    """

    df = pd.read_csv(path)

    if duplicated_column != "":
        df = df.drop_duplicates(duplicated_column)

    top_values = df.sort_values(sort_column, ascending = False).head(num)

    data_source = ColumnDataSource(top_values)

    return data_source


def csv_get_top_names(path, names_column, sort_column, num = 10):
    """Gera uma lista de nomes a partir de um arquivo .csv

    Lê o arquivo .csv, o transforma em um data frame e remove
    os nomes repetidos da coluna de nomes selecionada, depois
    ordena os valores a partir da coluna de ordenação e retorna
    uma lista com a quantidade definida dos primeiros nomes.

    Parametros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        names_column: str
            Deve conter o nome da coluna a ter os nomes coletados. 
            Deve conter exatamente um valor.
        sort_column : str
            Deve conter a coluna a qual haverá a ordenação dos valores.
            Deve conter exatamente um valor.
        num : int, optional
            Deve conter a quantidade de observações coletadas a partir
            da ordenação de valores (Por padrão 10).

        Retorna
        -------
        names
            Retorna a lista contendo os primeiros nomes obtidos através
            da ordenação.
    """

    df = pd.read_csv(path)
    df = df.drop_duplicates(names_column)

    sorted_df = df.sort_values(sort_column, ascending = False).head(num)
    
    names = []

    for each_name in sorted_df[names_column]:
        names.append(each_name)
    names.reverse()

    return names


def histogram_count(path, column, bins = 10, proportion_column = "",
                    base_proportion = 1, interval = [0, 1]):
    """Gera dados para criar um histograma a partir de um .csv

    Lê o arquivo csv, gera os dados para a criação do histograma
    a partir do numpy, é possível alterar a quantidade de barras do
    histograma, seu intervalo e sua proporção, retorna uma tupla 
    com os intervalos e a contagem dos intervalos.

    Parametros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        column : str
            Deve conter a coluna a qual haverá a contagem de ocorrências
            para o histograma.
            Deve conter exatamente um valor.
        bins : int, optional
            Deve conter a quantidade de barras do histograma
            (Por padrão 10).
        proportion_column : str, optional
            Caso haja uma outra coluna para parear a proporção
            do histograma, o valor da sua maior barra será
            proporcional ao maior valor desta coluna.
        base_proportion : float, optional
            Deve conter um número que indique a proporção base
            do histograma (Por padrão 1/100%).
        interval : list, optional
            Deve conter uma lista com o intervalo do eixo x do 
            Histograma, sendo o primeiro valor o início e o
            segundo o fim (Por padrão [0, 1]).

        Retorna
        -------
        (count, intervals)
            Retorna uma tupla contendo a contagem dos intervalos
            como primeiro valor e os intervalos como segundo.
    """

    df = pd.read_csv(path)
    data = df[column]

    hist_count = np.histogram(data, bins = bins, range = interval)
    intervals = hist_count[1]
    count = hist_count[0]

    if proportion_column != "":
        max_value = df[proportion_column].max()
        proportion = max_value / max(count)
        count = count * proportion
    count = count * base_proportion

    return count, intervals
