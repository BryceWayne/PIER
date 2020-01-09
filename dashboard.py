import numpy as np
from bokeh.io import curdoc, output_file
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Range1d, LinearColorMapper
from bokeh.models.widgets import Slider, TextInput, Tabs, Panel, Button, DataTable, Div, CheckboxGroup
from bokeh.models.widgets import NumberFormatter, TableColumn, Dropdown, RadioButtonGroup, Select
from bokeh.plotting import figure
from pprint import pprint
import os
import pandas as pd

SIZE = 800
""" GET DATA """
data2 = pd.read_csv('PIER/data/A15226.txt', sep="\t")
# print(data2.head)
data2 = data2.iloc[1:].dropna()
data2['Date'] = pd.to_datetime(data2['Date local DST']).dropna()
# print(data2.columns)
DATES = data2['Date'].tolist()
dates, times = [], []
for _ in DATES:
    dates.append(_.date())
    times.append(_.time())
t, times = times, []
for time in t:
    times.append(60*60*time.hour + 60*time.minute + time.second + time.microsecond/1E6)
data2['Date'] = dates
data2['Time'] = times
data2 = data2[['Date', 'Time', 'Depth (m)', 'Temp (C)']]
data2.columns = ['Date', 'Time', 'D', 'T']
# data2.head()

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
source1 = ColumnDataSource(data2)

"""
SETUP PLOTS
"""
plot1 = figure(plot_height=SIZE, plot_width=int(phi*SIZE), title="Depth vs. Date", tools="save", x_axis_type="datetime")
color_mapper1 = LinearColorMapper(palette='Magma256', low=max(source1.data['T']), high=min(source1.data['T']))
plot1.circle(x='Date', y='D', source=source1, color={'field': 'D', 'transform': color_mapper1})
plot1.y_range.flipped = True

plot2 = figure(plot_height=SIZE, plot_width=int(phi*SIZE), title="Depth vs. Time", tools="save")
color_mapper2 = LinearColorMapper(palette='Magma256', low=max(source1.data['D']), high=min(source1.data['D']))
plot2.circle(x='Time', y='D', source=source1, color={'field': 'D', 'transform': color_mapper2})
plot2.y_range.flipped = True
"""
SETUP WIDGETS
"""
div1 = Div(text="""<p style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
                    This plot is designed to give you an idea of what a Bokeh dashboard would provide.</p>""",
                    width=300, height=130)
"""
Set up callbacks
"""




# Set up layouts and add to document
inputs1 = column(div1)
tab1 = row(inputs1, plot1, width=int(phi*SIZE))
tab1 = Panel(child=tab1, title="Entire Data")
tab2 = Panel(child=row(plot2), title='Daily')
tabs = Tabs(tabs=[tab1, tab2])

curdoc().title = "P.I.E.R. Dashboard"
curdoc().theme = 'caliber'
curdoc().add_root(tabs)
