def figure_generator_gustavo(final_figure):

    final_figure.background_fill_color = "#efefef"
    final_figure.background_fill_alpha - 0.7
    final_figure.title.text_font_size = '20px'
    final_figure.title.text_font_style = 'bold'
    final_figure.title.align = 'center'
    final_figure.axis.axis_label_text_font_size = '16px'
    final_figure.xaxis.axis_label_standoff = 25
    final_figure.xaxis.axis_label_standoff = 15
    final_figure.grid.grid_line_color = None
    final_figure.min_border_right = 50
    
    return final_figure

def figure_text_generator_sillas(figure):

    figure.background_fill_color="GhostWhite"

    figure.title.text_color = "Black"
    figure.title.text_font = "Arial Black"
    figure.title.text_font_size = "18px"
    figure.title.align = "center"

    figure.xaxis.axis_label_text_font = "Arial"
    figure.xaxis.axis_label_text_font_size = "14px"
    figure.xaxis.axis_label_text_font_style = "normal"

    figure.yaxis.axis_label_text_font = "Arial"
    figure.yaxis.axis_label_text_font_size = "14px"
    figure.yaxis.axis_label_text_font_style = "normal"

    return figure