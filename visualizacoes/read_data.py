'''Módulo de leitura do arquivo .csv com os dados

Este módulo contém funções de manipulação de dados. 
Como funções para gerar objetos ColumnDataSource a partir de um arquivo .csv e 
funções que manipulam dataframes

Funcionalidades:
- csv_to_columndatasouce: gera um objeto ColumnDataSource a partir de um arquivo .csv
- csv_get_top: gera um objeto ColumnDataSource a partir de um arquivo .csv
- csv_get_top_names: gera uma lista de nomes a partir de um arquivo .csv
- histogram_data: gera dados para criar um histograma a partir de um .csv
- column_as_size: gera um dataframe do pandas a partir de um arquivo .csv
- csv_filter_by_name_to_cds: filtra dados de uma linha de um .csv e retorna um ColumnDataSource
- get_column_observations: gera uma lista com os dados de uma coluna especificada de um arquivo .csv
- get_statistic_by_year: gera um ColumDataSource e uma lista com as estatísticas do ano a partir de um arquivo .csv
- columndatasource_plot3_gustavo: gera um objeto dataframe a partir de um arquivo .csv
- columndatasource_plot2_gustavo: gera um objeto ColumnDataSource a partir de um arquivo .csv
- columndatasource_plot1_gustavo: gera um objeto ColumnDataSource a partir de um arquivo .csv
'''

# Importando as bibliotecas usadas nesse modulo
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource

def csv_to_columndatasource(path, colunas = []):
    '''Gera um objeto ColumnDataSource a partir de um arquivo .csv

    Lê o arquivo .csv, armazenando o conteudo dele em um dataframe do 
    pandas, então seleciona as colunas desejadas (todas por padrão) e 
    gera um objeto ColumnDataSource corespondente. O objeto gerado pode
    ser usado para elaboração das visualizações com a biblioteca bokeh.

    Parâmetros
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
        >>> csv_to_columndatasource("data/spotify_youtube_year.csv", ['Artist, 'Track'])
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

    Parâmetros
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
    uma lista com a quantidade definida dos primeiros nomes, se
    apenas um nome for selecionado, retorna apenas a string
    do primeiro valor.

    Parâmetros
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

    if num == 1:
        names = names[0]

    return names

    return names

def histogram_data(path, column, start = 0, end = 1, bins = 10, proportion_column = "",
                    base_proportion = 1):
    """Gera dados para criar um histograma a partir de um .csv

    Lê o arquivo csv, gera os dados para a criação do histograma
    a partir do numpy, é possível alterar a quantidade de barras do
    histograma, seu começo, fim e sua proporção, retorna um
    ColumnDataSource contendo os parâmetros "top", a altura
    do histograma, "start", os pontos do lado esquerdo e "end",
    os pontos do lado direito.

    Parâmetros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        column : str
            Deve conter a coluna a qual haverá a contagem de ocorrências
            para o histograma.
            Deve conter exatamente um valor.
        start : int, optional
            Deve conter o ponto do eixo em que seu histograma começa.
            (Por padrão 0).
        end : int, optional
            Deve conter o ponto do eixo em que seu histograma termina.
            (Por padrão 1).
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

        Retorna
        -------
        values
            Retorna um ColumnDataSource contendo os valores da
            altura dos quadrados, "top", os pontos esquredos,
            "start" e os pontos direitos, "end" para a geração
            do histograma a partir do ".quad()".
    """

    df = pd.read_csv(path)
    data = df[column]
    interval = [start, end]

    hist_count = np.histogram(data, bins = bins, range = interval)
    intervals = hist_count[1]
    count = hist_count[0]
    starts = intervals[:-1]
    ends = intervals[1:]

    if proportion_column != "":
        max_value = df[proportion_column].max()
        proportion = max_value / max(count)
        count = count * proportion
    count = count * base_proportion

    values = {"top": count, "start": starts,
              "end": ends}

    return ColumnDataSource(values)


def column_as_size(dataframe, column, parameter):
    """Gera um data frame do pandas a partir de um arquivo .csv

    Lê o arquivo .csv, o transforma em um data frame do pandas, e cria uma nova
    coluna chamada "size" a partir de uma coluna e do parâmetro selecionados. Atribui
    à coluna "size" os valores da coluna indicada divididos pelo parâmetro. E retorna
    o data frame.

    Parametros  
        ----------
        dataframe : pandas.DataFrame
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
        df
            Retorna o data frame com a nova coluna.
    """
    
    if 'size' not in dataframe.columns:
        dataframe["size"] = dataframe[column] / parameter

        return dataframe

def csv_filter_by_name_to_cds(path, filter_column, value, lowercase = False):
    """Filtra dados de uma linha de um .csv e retorna um ColumnDataSource

    Lê o arquivo csv, seleciona apenas a linha que contém o valor
    e gera um dicionário com as chaves "Columns" que contém o nome
    das colunas e "Values" que contém os valores das colunas na
    linha selecionada, retorna um ColumnDataSource feito a partir
    desse dicionário, caso lowercase esteja ativado, a busca é feita
    independente do tipo de caixa da palavra procurada.

    Parâmetros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        filter_column : str
            Deve indiicar o nome da coluna que contém o valor procurado.
            Deve conter exatamente um valor.
        value : str
            Deve indicar o valor procurado na coluna que retornará a linha.
            Deve conter exatamente um valor.
        lowercase : bool, optional
            Deve indicar se é necessária a realização da busca com o caso
            de caixa baixa.

        Retorna
        -------
        filtered_data, selected_row
            Retorna uma tupla contendo o ColumnDataSource do 
            dicionário gerado a partir das Colunas e dos Valores 
            da linha filtrada, que possui como chaves as strings 
            "Columns" e "Values" e um ColumnDataSource da linha 
            selecionada.
    """

    df = pd.read_csv(path)
    df.drop_duplicates(filter_column, inplace = True)
    if lowercase == False:
        selected_row = df[df[filter_column] == value]
    else:
        selected_row = df[df[filter_column].apply(str.lower) == value.lower()]

    columns = selected_row.columns
    values = selected_row.values[0]

    filtered_data = {"Columns": columns,
                     "Values": values}

    return ColumnDataSource(filtered_data), ColumnDataSource(selected_row)

def get_column_observations(path, column, sort_column = "", lowercase = False):
    """Gera uma lista com os dados de uma coluna especificada de um arquivo .csv
    
    Lê o arquivo csv, seleciona os dados de uma coluna, caso haja uma coluna
    de ordenação, ordena os dados com base nela, caso lowercase seja verdadeira,
    retorna todos os valores como caixa baixa.

    Parâmetros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        column : str
            Deve indicar a coluna onde será feita a coleta das observações.
            Deve conter exatamente um valor.
        sort_column: str, optional
            Deve conter a coluna por onde a ordenação deve ser feita,
            se necessário.
        lowercase : bool, optional
            Deve indicar se é necessária a realização da busca com o caso
            de caixa baixa.

        Retorna
        -------
        values
            Uma lista contendo os valores da coluna coletados a partir
            dos parâmetros definidos.
    """

    df = pd.read_csv(path)
    df.drop_duplicates(column, inplace = True)

    if sort_column != "":
        df = df.sort_values(sort_column, ascending = False)
    
    values = []
    if lowercase == False:
        for value in df[column]:
            values.append(value)
    else:
        for value in df[column]:
            values.append(value.lower())

    return values

def get_statistic_by_year(path, years_column, target_column, interval = [1960, 2021],
                          method = "mean"):
    """Gera um ColumDataSource e uma lista com as estatísticas do ano a partir de um arquivo .csv

    Lê o arquivo csv, ordena os dados do ano mais antigo para o mais recente,
    e filtra para os anos do intervalo selecionado (Pré-definido de 1960 à 2021),
    gera a lista dos anos e gera os valores a partir do agrupamento por ano e
    da aplicação do método selecionado (Por padrão a média) na coluna dos
    valores desejados.

    Parâmetros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        years_column : srt
            Deve indicar a coluna dos anos da base de dados.
            Deve conter exatamente um valor.
        target_column : str
            Deve indicar a coluna onde será feita a coleta dos valores.
            Deve conter exatamente um valor.
        interval : list, optional
            Deve conter uma lista com o intervalo dos anos da coleta, sendo
            o primeiro valor o ano inicial e o segundo o ano final
            (Por padrão [1960, 2021]).
        method : str, optional
            Deve indicar o método da coleta de valores, possíveis métodos são
            a média ("mean"), a soma ("sum") e a contagem ("count")
            (Por padrão "mean").

        Retorna
        -------
        result
            Retorna o dicionário result como ColumnDataSource, que contém
            "Values", os valores coletados, e "Years" os anos em que foram
            feitas as coletas, e years.
    """

    df = pd.read_csv(path)
    df = df.sort_values(years_column)
    data = df[(df[years_column] >= interval[0]) & (df[years_column] <= interval[1])]

    years = data[years_column].unique()
    years = list(years)

    if method == "mean":
        values = data.groupby(years_column)[target_column].mean()
    elif method == "sum":
        values = data.groupby(years_column)[target_column].sum()
    elif method == "count":
        values = data.groupby(years_column)[target_column].count()
    
    values = list(values)

    result = {"Values": values,
              "Years": years}

    return ColumnDataSource(result)

def columndatasource_plot1_gustavo(datapath):
    '''Gera um objeto ColumnDataSource a partir de um arquivo .csv

    Lê o arquivo .csv, armazenando o conteudo dele em um dataframe do 
    pandas, então manipula o dado de acordo com o necessário para a execução
    do plot 1 do gustavo e gera um objeto ColumnDataSource corespondente, que só
    deve ser usado para o plot citado. 

    Parâmetros
        ----------
        datapath : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.

        Retorna
        -------
        columndatasource:
            Retorna o ColumnDataSource gerado a partir dos paramentros fornecidos.

        Examples
        --------
        >>> columndatasource_plot1_gustavo("data/spotify_youtube_year_year.csv")
    '''

    df = pd.read_csv(datapath) #lê o csv

    df.rename(columns={'release_date': 'year'}, inplace=True) #renomeia a coluna, para melhor legibilidade do código.

    df['year'] = pd.to_datetime(df['year'], format='%Y') #transforma a o interio yyyy (ex: 2020), em datetime.

    df.drop_duplicates('Track', inplace= True) #retira as musicas duplicadas

    df_by_year = df.groupby('year').count() #agrupa por ano e conta a quantidade de musicas em cada ano

    columndatasource = ColumnDataSource(df_by_year) #transforma o dataframe em ColumnDataSource

    return columndatasource

def columndatasource_plot2_gustavo(datapath):
    '''Gera um objeto ColumnDataSource a partir de um arquivo .csv

    Lê o arquivo .csv, armazena em um dataframe do pandas e filtra o
    dataframe pelas 100 musicas mais vistas. Essa manipulação é 
    especifica para a execução do plot 2 do gustavo e gera um objeto 
    ColumnDataSource corespondente, que só deve ser usado para o plot citado. 

    Parâmetros
        ----------
        datapath : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.

        Retorna
        -------
        columndatasource:
            Retorna o ColumnDataSource gerado a partir dos paramentros fornecidos.

        Examples
        --------
        >>> columndatasource_plot2_gustavo("data/spotify_youtube_year_year.csv")
    '''

    df = pd.read_csv(datapath) #lê o csv

    df_views_por_track = df.sort_values(by = 'Views', ascending=False).drop_duplicates('Track') #organiza os dados em ordem decresente na coluna 'Views'. Também retira as míúsicas duplicadas

    df_100_mais_vistos_completo = (df_views_por_track).head(100) #cria um dataframe contendo apenas as 100 musicas com mais views

    df_100_mais_vistos_completo.loc[:, 'Views'] = df_100_mais_vistos_completo['Views']/1000000 #divide o valor de 'Views' por 1M, para ter o valor em milhoes de views

    columndatasource = ColumnDataSource(df_100_mais_vistos_completo) #transforma o dataframe em ColumnDataSource

    return columndatasource

def columndatasource_plot3_gustavo(datapath):
    '''Gera um objeto dataframe a partir de um arquivo .csv

    Lê o arquivo .csv, armazena em um dataframe do pandas e
    transforma a coluna 'official_video' em string. Essa função
    prepara os dados para o uso da função boxplot, que gerará
    o plot 3 do gustavo. 

    Parâmetros
        ----------
        datapath : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.

        Retorna
        -------
        df:
            Retorna o dataframe gerado a partir dos paramentros fornecidos.

        Examples
        --------
        >>> columndatasource_plot3_gustavo("data/spotify_youtube_year_year.csv")
    '''

    df = pd.read_csv(datapath) #lê o csv

    df['official_video'] = df['official_video'].astype(str) #transforma os valores true e false (boleanos) da coluna, para o tipo string.

    return df

def columndatasource_plot1_marciano(path):
    """Retorna um column data source de um arquivo .csv
    
    Lê o arquivo csv, manipula os dados, assim como explicado nos
    comentários do código, e retorna um ColumDataSource

    Parâmetros
        ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
    
        Retorna
        -------
        data_source_1
            ColumnDataSource pronto para a plotagem do gráfico
    """
    data = pd.read_csv(path) # Lendo o .csv como um data frame do pandas

    color = [] # Criando lista vazia para posteriormente tranformar em coluna que define a cor dos glifos.

    for each_float in data["Liveness"]: # Loop para percorrer a coluna Liveness, e dependendo se o valor é maior que 0.8 é
        if each_float >= 0.8:          # maior ou menor que 0.8, adiciona a palavra Blue ou Gray na lista vazia criada acima.
            color.append("Blue")
        else:
            color.append("Gray")

    data["color"] = color # Criando a coluna que irá definir a cor dos glifos baseada na lista criada acima

    data_source_1 = ColumnDataSource(data) # Tranforma o data frame em ColumDataSource

    return(data_source_1)



def columndatasource_plot2_marciano(path):
    """Retorna um column data source de um arquivo .csv
        
    Lê o arquivo csv, manipula os dados, assim como explicado nos
    comentários do código, e retorna um ColumDataSource

    Parâmetros
         ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        
        Retorna
        -------
        data_source_2
            ColumnDataSource pronto para a plotagem do gráfico
        music_duration_mean
            Média de duração das músicas em todos os anos
    """
    data = pd.read_csv(path) # Lendo o .csv como um data frame do pandas

    data["Duration_s"] = data["Duration_ms"]/1000 # Mudando a coluna Duration_ms para segundos (dividindo por 1000)

    duration_by_year = pd.DataFrame(data.groupby(["release_date"])["Duration_s"].mean()) # Agrupando por ano de lançamento e calculando a média de
                                                                                        # duração das músicas por ano em um pd.Series transformado em DataFrame

    count_by_year = pd.DataFrame(data.groupby(["release_date"])["Track"].count())  # Agrupando por ano de lançamento e contando o número de
                                                                                # músicas por ano em um pd.Series transformado em DataFrame


    data_by_year = duration_by_year                         # Linhas para juntar os DataFrames em um só
    data_by_year["Track Count"] = count_by_year["Track"]

    data_by_year_filtered = data_by_year[data_by_year['Track Count'] > 90] # Filtrando o DataFrame para os anos com mais de 90 músicas

    data_source_2 = ColumnDataSource(data_by_year_filtered) # Transformando em ColumnDataSource

    music_duration_mean = data_by_year["Duration_s"].mean()

    return(data_source_2, music_duration_mean)



def columndatasource_plot3_marciano(path):
    """Retorna um column data source de um arquivo .csv
        
    Lê o arquivo csv, manipula os dados, assim como explicado nos
    comentários do código, e retorna um ColumDataSource

    Parâmetros
         ----------
        path : str, path object or file-like object
            Deve indicar o local onde está armazenado o .csv a ser lido. 
            Deve conter exatamente um valor.
        
        Retorna
        -------
        data_source_3
            ColumnDataSource pronto para a plotagem do gráfico

        lista_top30_artistas
            Lista para fazer o label dos artistas no eixo Y
    """
    data = pd.read_csv(path) # Lendo o .csv como um data frame do pandas

    data = data.dropna(subset=['Stream']) # Removendo as músicas que não possuiam o númeoro de streams

    stream_by_artist = pd.DataFrame(data.groupby(["Artist"])["Stream"].mean().sort_values().tail(30)) # Agrupando por artista, calulando a média de streams,
                                                                                                    # ordenando da menor para a maior nº de streams e deixando
                                                                                                    # somente as últimas 30 linhas do data frame.

    stream_by_artist["stream_label"]= stream_by_artist["Stream"]/1000000000 # Criando coluna para as labels nas barras
    stream_by_artist["stream_label"] = stream_by_artist["stream_label"].round(2).astype(str) # Deixando com somente duas casas deciamais
    stream_by_artist["stream_label"] = stream_by_artist["stream_label"] + " bi"  # Adicionando "bi" na frente do número

    data_source_3 = ColumnDataSource(stream_by_artist) # Transformando em ColumnDataSource

    lista_top30_artistas = stream_by_artist.index.tolist()

    return(data_source_3, lista_top30_artistas)
