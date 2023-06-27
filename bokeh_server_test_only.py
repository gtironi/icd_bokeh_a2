from bokeh.models import Select, ColumnDataSource, Paragraph, Div
from bokeh.io import curdoc, show
from bokeh.layouts import row, gridplot,column
from bokeh.plotting import figure
from numpy.random import random, normal

initial_points = 500

data_points = ColumnDataSource(data = {'x': random(initial_points), 'y': random(initial_points)})

plot = figure(title = "Scatterplot", align = "center")

plot.diamond(x = 'x', y = 'y', source = data_points, color = 'red')

select_widget = Select(title="Select:", value = "uniform distribution", options=["uniform distribution", "normal distribution"])

def callback(attr, old, new):
    if select_widget.value == "uniform distribution":
        function = random
    else:
        function = normal
    data_points.data = {'x': function( size = initial_points), 'y': function( size = initial_points)}

select_widget.on_change('value', callback)

escrita = Paragraph(text = "Learn how to create and deploy a stock price comparison web app with Bokeh. Use your Python Bokeh visualization skills to create a practical, interactive tool.")

div = Div(text="""<a href="https://www.geeksforgeeks.org/python-programming-language/">
Python</a> is <b>high level</b> programming language.
Its easy to learn because of its syntax.""")

row1 = row(select_widget, plot)

select_layout = column(row1, escrita, div)

curdoc().add_root(select_layout)