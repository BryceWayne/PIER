import numpy as np
from bokeh.io import curdoc, output_file
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput, Tabs, Panel, Button, DataTable, Div, CheckboxGroup
from bokeh.models.widgets import NumberFormatter, TableColumn, Dropdown, RadioButtonGroup, Select
from bokeh.plotting import figure
from pprint import pprint
import pandas as pd


"""
SETUP DATA
"""
N = 1000
sigma = 1
pi = np.pi
phi = 1.618
ratio = 0
mu = 0
x1 = np.linspace(mu - 6 * sigma, mu + 6 * sigma, N)
y1 = 1/(sigma*np.sqrt(2*pi))*np.exp(-0.5*((x1-mu)/sigma)**2)
source1 = ColumnDataSource(data=dict(x=x1, y=y1))

"""
SETUP PLOTS
"""
plot1 = figure(plot_height=600, plot_width=int(phi*600), title="Oh my Gauss",
              tools="save", x_range=[x1.min(), x1.max()], y_range=[0, phi*y1.max()])
plot1.line('x', 'y', source=source1, line_width=3, legend_label="Your Gauss")

"""
SETUP WIDGETS
"""
div1 = Div(text="""<p style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
                    Oh My Gauss is designed to let you explore what various kinds of normal distributions look like. 
                    Try changing the Standard Deviation or Average to see how this affects the plot.</p>""",
                    width=300, height=130)
"""
Set up callbacks
"""




# Set up layouts and add to document
inputs1 = column(div1)
tab1 = row(inputs1, plot1, width=int(phi*400))
tab1 = Panel(child=tab1, title="Example")
tabs = Tabs(tabs=[tab1])

curdoc().title = "P.I.E.R. Dashboard"
curdoc().theme = 'caliber'
curdoc().add_root(tabs)
