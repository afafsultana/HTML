from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
import pandas as pd
from bokeh.charts import Bar, output_file, show
from bokeh.sampledata.autompg import autompg as df
from flask import *
from flask import Flask, render_template
import random
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components

app = Flask(__name__)
@app.route('/')
@app.route("/tables")

def show_tables():

	db = create_engine(URL(**settings.DATABASE))
	row=pd.read_sql_query('select date, sports from sports_livesum',con=db, parse_dates=['date'])
		y = (row.sports)
        x = (row.date)
	p = figure(title='A Bokeh plot', plot_width=500, plot_height=400,x_axis_type="datetime")
        p.logo = None
        p.toolbar_location = None
	p.line(x,y)
	p.xaxis.axis_label = "date"
	p.yaxis.axis_label = "sports"
	figJS,figDiv = components(p,CDN)
	
	return(render_template(
	'figures.html',tables=[row.to_html(classes='sport')],titles = ['date','sport'],
	y=y,
	figJS=figJS,
	figDiv=figDiv))       

if __name__ == "__main__":
    app.run(debug=True)
