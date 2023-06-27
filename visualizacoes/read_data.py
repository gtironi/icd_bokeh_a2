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
        duplicated_column : str
            Deve conter o nome de uma coluna da base de dados, a qual
            possui valores duplicados
        num : int
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
        num : int
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

    return names


def column_as_size(path, column, parameter):
    """Gera um objeto ColumnDataSource a partir de um arquivo .csv

    Lê o arquivo .csv, o transforma em um data frame do pandas, e cria uma nova
    coluna chamada "size" a partir de uma coluna e do parâmetro selecionados. Atribui
    à coluna "size" os valores da coluna indicada divididos pelo parâmetro. E retorna
    um ColumDataSource desse data frame.

    Parametros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        column : str
            Deve conter o nome de uma coluna da base de dados, a qual
            será feita a divisão.
            Deve conter exatamente um valor.
        parameter : float
            Deve conter o número que será feita a divisão da coluna.
            Deve conter exatamente um valor.

        Retorna
        -------
        data_source
            Retorna o ColumnDataSource gerado a partir do data frame
            com a nova coluna.
    """

    df = pd.read_csv(path)

    if 'size' not in df.columns:
        df["size"] = df[column] / parameter
        data_source = ColumnDataSource(df)

        return data_source