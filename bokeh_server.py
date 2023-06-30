
from bokeh.models import Select, Div
from bokeh.layouts import column
from bokeh.plotting import curdoc
from visualizacoes.visualizacoes_sillas import gera_layout_sillas
# from visualizacoes.visualizacoes_marciano import cria_layout_marciano


# def gera_bokeh_server(path):
path = "visualizacoes/data/spotify_youtube_year.csv"

Layout_Sillas = gera_layout_sillas(path)
# Layout_Marciano = visualizacoes.visualizacoes_marciano.cria_layout_marciano()

layouts = [Layout_Sillas]

# select_button_layout = Select(title = "Selecione um dos layouts, o carregamento pode demorar um pouco.", value = "",
#                                   options = layouts, width = 1300)
    
home_page_text = "<h3>somethign<h3>"

home_page_div = Div(text = home_page_text,
                        style = {'text-align': 'justify', 'font-size': '16px'}, width=580, margin=(0, 40, 50, 40))

main_page = column(home_page_div, Layout_Sillas)

# Layout_Sillas.visible = False
# Layout_Marciano.visible = False

# def update_layout(attr, old, new):
#     selected_layout = select_button_layout.value
#     home_page_div.visible = False
#     Layout_Sillas.visible = False
#     # Layout_Marciano.visible = False

#     selected_layout.visible = True

# select_button_layout.on_change("value", update_layout)

curdoc().add_root(main_page)


