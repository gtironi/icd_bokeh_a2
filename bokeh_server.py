
from bokeh.models import Select, Div
from bokeh.layouts import column, row
from bokeh.plotting import curdoc
from visualizacoes.visualizacoes_marciano import cria_layout_marciano
from visualizacoes.visualizacoes_gustavo import cria_layout_gustavo
from visualizacoes.visualizacoes_sillas import gera_layout_sillas
from visualizacoes.visualizacoes_leonardo import gera_layout_leonardo

# path = "visualizacoes/data/spotify_youtube_year.csv"

def gera_bokeh_server(path):

    layout_sillas = gera_layout_sillas(path)
    layout_marciano = cria_layout_marciano(path)
    layout_gustavo = cria_layout_gustavo(path)
    layout_leonardo = gera_layout_leonardo(path)

    
    layout_sillas.visible = False
    layout_marciano.visible = False
    layout_gustavo.visible = False
    layout_leonardo.visible = False


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

    
    layouts = {"Home Page": home_page_div,
               "Sillas": layout_sillas,
               "Marciano": layout_marciano,
               "Gustavo": layout_gustavo,
               "Leonardo": layout_leonardo}
    
    layouts_list = list(layouts.values())

    select_button_layout = Select(title = "Selecione um dos layouts, o carregamento pode demorar um pouco.",
                                  value = "Home Page" , options = ["Home Page","Sillas", "Marciano", "Gustavo", "Leonardo"], width = 1400)

    def update_layout(attr, old, new):
        selected_layout = layouts[select_button_layout.value]

        for layout in layouts_list:
            if layout != selected_layout:
                layout.visible = False
        selected_layout.visible = True


    select_button_layout.on_change("value", update_layout)
    
    main_page = column(row(select_button_layout), row(home_page_div, layout_sillas, layout_marciano, layout_leonardo, layout_gustavo))

    return main_page


page = gera_bokeh_server("visualizacoes/data/spotify_youtube_year.csv")

curdoc().add_root(page)

