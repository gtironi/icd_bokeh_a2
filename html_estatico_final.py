from bokeh.models import Div
from bokeh.layouts import column
from bokeh.io import output_file
from visualizacoes.visualizacoes_marciano import cria_layout_marciano
from visualizacoes.visualizacoes_gustavo import cria_layout_gustavo
from visualizacoes.visualizacoes_estaticas_sillas import gera_layout_estatico_sillas
from visualizacoes.visualizacoes_leonardo import gera_layout_leonardo

# path = "visualizacoes/data/spotify_youtube_year.csv"

def gera_html(path):

    output_file("index.html")

    layout_sillas = gera_layout_estatico_sillas(path)
    layout_marciano = cria_layout_marciano(path)
    layout_gustavo = cria_layout_gustavo(path)
    layout_leonardo = gera_layout_leonardo()
        
    home_page_text = """<h3 id="trabalho-de-introdu-o-ci-ncia-de-dados-">Trabalho de Introdução à ciência de dados:</h3>
    <p>Os alunos Leonardo Alexandre, Sillas Rocha, Gustavo Tironi e Luís Felipe elaboraram visualizações a partir de uma base e dados, encontrada no Kaggle, sobre músicas do Spotify e do YouTube.
    A base de dados possui diversas variáveis, como autor, nome, data de lançamento e duração.
    Além disso, contém variáveis pouco conhecidas. Algumas estão listadas abaixo.</p>
    <ul>
    <li>popularity: Popularidade das músicas.</li>
    <li>release_year: Ano de lançamento da música.</li>
    <li>Stream: O número de vezes que a música foi escutada no Spotify</li>
    <li>Energy: Quão energizada uma música está na faixa de 0 a 1.</li>
    <li>Loudness: Quão alto é uma música em db.</li>
    <li>Danceability: Quão dançável uma música é na faixa de 0 a 1.</li>
    <li>Acousticness: Quão acústica é uma faixa na faixa de 0 a 1.</li>
    <li>Valence: A positividade da música na faixa de 0 a 1.</li>
    <li>Liveness: A presença de público na música no intervalo de 0 a 1.</li>
    </ul>
    """

    espaço_sillas = Div(text = 'Gráficos Sillas', height=120, style = {'text-align': 'center', 'font-size': '70px'}, margin=(40, 0, 40, 0), align = 'center')

    espaço_gustavo = Div(text = 'Gráficos Gustavo', height=120, style = {'text-align': 'center', 'font-size': '70px'}, margin=(40, 0, 40, 0), align = 'center')

    espaço_marciano = Div(text = 'Gráficos Marciano', height=120, style = {'text-align': 'center', 'font-size': '70px'}, margin=(40, 0, 40, 0), align = 'center')

    espaço_leonardo = Div(text = 'Gráficos leonardo', height=120, style = {'text-align': 'center', 'font-size': '70px'}, margin=(40, 0, 40, 0), align = 'center')

    home_page_div = Div(text = home_page_text,
                            style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 0, 0, 450))

    main_page = column(home_page_div, espaço_sillas, layout_sillas, espaço_marciano, layout_marciano, espaço_gustavo, layout_gustavo, espaço_leonardo, layout_leonardo)

    return main_page
