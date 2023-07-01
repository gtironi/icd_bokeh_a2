import pandas as pd
from plot_style import figure_generator_gustavo

from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

def boxplot(dataframe, eixo_x, eixo_y):

    # Determina os valores categoricos que aparecerão no eixo x
    valores_x = list(dataframe[eixo_x].unique())
    valores_x.remove('nan') 

    # Calcula os quantils
    df_quantils = dataframe.groupby(eixo_x)[eixo_y].quantile([0.25, 0.5, 0.75])
    df_quantils = df_quantils.unstack().reset_index()
    df_quantils.columns = [eixo_x, "q1", "q2", "q3"]
    dataframe = pd.merge(dataframe, df_quantils, on=eixo_x, how="left")

    # Calcula a distância interquantils e os limites do boxplot (fator: 1,5)
    iqr = dataframe.q3 - dataframe.q1
    dataframe["upper"] = dataframe.q3 + 1.5*iqr
    dataframe["lower"] = dataframe.q1 - 1.5*iqr

    # Transforma o df em ColumnDataSource
    source = ColumnDataSource(dataframe)

    # Cria a figura que será usada
    boxplot = figure_generator_gustavo(figure(height=480, width=690, x_range=valores_x, tools="", toolbar_location=None,
            y_range = (dataframe[eixo_y].min(), dataframe[eixo_y].max())))
    

    # Adicona as linhas do boxplot à figura
    whisker = Whisker(base=eixo_x, upper="upper", lower="lower", source=source)
    whisker.upper_head.size = whisker.lower_head.size = 20
    boxplot.add_layout(whisker)

    # Adicona o corpo do boxplot à figura
    cmap = factor_cmap(eixo_x, ['#AF601A',  '#C70039'], valores_x)
    boxplot.vbar(eixo_x, 0.7, "q2", "q3", source=source, color=cmap, line_color="black")
    boxplot.vbar(eixo_x, 0.7, "q1", "q2", source=source, color=cmap, line_color="black")

    # Adicona os outliers à figura
    outliers = dataframe[~dataframe[eixo_y].between(dataframe.lower, dataframe.upper)]
    boxplot.scatter(eixo_x, eixo_y, source=outliers, size=6, color="black", alpha=0.3)

    return boxplot