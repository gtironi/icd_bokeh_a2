
from bokeh.models import Select, Div
from bokeh.layouts import column
from bokeh.plotting import curdoc
from visualizacoes.visualizacoes_marciano import cria_layout_marciano
from visualizacoes.visualizacoes_gustavo import cria_layout_gustavo
from visualizacoes.visualizacoes_sillas import gera_layout_sillas

# path = "visualizacoes/data/spotify_youtube_year.csv"

def gera_bokeh_server(path):

    Layout_Sillas = gera_layout_sillas(path)
    Layout_Marciano = cria_layout_marciano(path)
    Layout_Gustavo = cria_layout_gustavo(path)

    # layouts = [Layout_Sillas]

    # select_button_layout = Select(title = "Selecione um dos layouts, o carregamento pode demorar um pouco.", value = "",
    #                                   options = layouts, width = 1300)
        
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

    home_page_div = Div(text = home_page_text,
                            style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))

    main_page = column(home_page_div, Layout_Sillas, Layout_Marciano, Layout_Gustavo)

    # Layout_Sillas.visible = False
    # Layout_Marciano.visible = False

    # def update_layout(attr, old, new):
    #     selected_layout = select_button_layout.value
    #     home_page_div.visible = False
    #     Layout_Sillas.visible = False
    #     # Layout_Marciano.visible = False

    #     selected_layout.visible = True

    # select_button_layout.on_change("value", update_layout)

    return main_page


page = gera_bokeh_server("visualizacoes/data/spotify_youtube_year.csv")

curdoc().add_root(page)

