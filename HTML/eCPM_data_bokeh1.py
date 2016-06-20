from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
import pandas as pd
from bokeh.charts import Bar, output_file, show
from bokeh.embed import file_html, components
from bokeh.plotting import figure, output_file, show, gridplot, output_server
from bokeh.properties import Instance
from bokeh.models import NumeralTickFormatter, Axis, SingleIntervalTicker, LinearAxis, Grid, GridPlot, ColumnDataSource, FixedTicker
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, NumberFormatter, MultiSelect, Slider, DateRangeSlider
from bokeh.io import hplot, output_file, show, vform, vplot, curdoc
#from bokeh.server.app import bokeh_app
#from bokeh.server.utils.plugins import object_page
from datetime import date
import locale
from bokeh.client import session, push_session

def show_tables():


	db = create_engine(URL(**settings.DATABASE))
	row = pd.read_sql_query('select sales_channel, impressions, cpm, date from ecpm_data',con=db)
	row['bins_cpm'] = pd.qcut(row['cpm'], 13, labels=False)

	p = Bar(row,
	name='bar',
	values='impressions',
	label='bins_cpm',
	xlabel = 'eCPM_bin',
	ylabel = 'Impressions',
	stack='sales_channel',
	agg='sum',
	legend="top_right",
	title="Bokeh: eCPM_data", plot_width=800)

	session = push_session(curdoc())

	ds = r.data_source


def update():
	slider = Slider(ds.data ["cpm"], 1) 
	ds.data.update(cpm=slider)
	
	#add to slider if it doesn't work: start=0, end=10, value=1, step=.1, title="eCPM_bins", orientation = "vertical")
	# taken from example: rmin = roll(ds.data["inner_radius"], 1)
    # taken from example: rmax = roll(ds.data["outer_radius"], -1)
    


# p.outline_line_width = 7
# yaxis = p.select( dict(type=Axis, layout="left"))[0]
# yaxis.formatter = NumeralTickFormatter(format="0,0")
# yaxis.ticker = SingleIntervalTicker(interval=2500000, num_minor_ticks=10)
# xaxis = p.select(dict(type=Axis, layout="below"))[0]
# xaxis.formatter = NumeralTickFormatter(format="$0.00")

# #locale.setlocale(locale.LC_ALL, 'en_US')
# #d=locale.format("%d", row.impressions, grouping=True)
# source = ColumnDataSource(row)
# columns = [
        # TableColumn(field="date", title="Dates", formatter=DateFormatter()),
        # TableColumn(field="cpm", title="CPM", formatter=NumberFormatter(format="$0.00")),
        # TableColumn(field="impressions", title="Impressions",formatter=NumberFormatter()),
        # TableColumn(field="sales_channel", title="Sales_channel"),
        # TableColumn(field="bins_cpm", title="bins_cpm")
        # ]
# data_table = DataTable(source=source, columns=columns, width=800, height=810)
# multi_select = MultiSelect(title="Option:", value=["foo", "quux"], options=["foo", "bar", "baz", "quux"])       
#dateRange = Instance(DateRangeSlider)
#dateRange = DateRangeSlider(title="Period:", name="period", value=(26-08-2015,18-09-2015), bounds=(26-08-2015,18-09-2015), range=(dict(days=1), None))
#slider = Slider(start=0, end=10, value=1, step=.1, title="eCPM_bins", orientation = "vertical")

curdoc().add_periodic_callback(update, 30)
session.show() # open the document in a browser
session.loop_until_closed() # run forever


output_file("figures.html")

s = vplot(hplot(p,slider),multi_select,data_table)
show(s)

# renderer = p.select(dict(name='bar'))
# ds = renderer[0].data_source

# while True:
	# slider(ds.data["cpm"])
	# #cursession().store_objects(ds)
