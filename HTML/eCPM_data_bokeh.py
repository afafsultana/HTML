from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
import pandas as pd
from bokeh.charts import Bar, output_file, show
from flask import Flask, render_template
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from bokeh.plotting import figure, output_file, show, gridplot, output_server
from bokeh.models import NumeralTickFormatter, Axis, SingleIntervalTicker, LinearAxis, Grid, GridPlot, ColumnDataSource
from datetime import date
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, MultiSelect
from bokeh.io import output_file, show, vform

app = Flask(__name__)
@app.route('/')
@app.route("/tables")
@app.template_filter('datetime')
def show_tables():

	db = create_engine(URL(**settings.DATABASE))
	row = pd.read_sql_query('select sales_channel, impressions, cpm, date from ecpm_data',con=db)
	
	row['bins_cpm'] = pd.qcut(row['cpm'], 13, labels=False)
        #print pd.qcut(row['bins_cpm'], 13)
	#qry = row.filter(row.date.between('2015-27-08', '2015-29-09'))
	#qry = row.filter(row.date.between('2015-27-08', '2015-29-09'))
	#date = datetime.strptime('row.date', '%m/%d/%Y')
	#qry = row.date.filter(and_(date <= '09/29/2015', date >= '08/27/2015'))
	#row_filtered = row[row.date <= '09/29/2015']
	#print pd.dtype
	#print row.dtype
	#print row.columns
	#while True: 
	#multi_select = MultiSelect(title="Option:", value=["foo", "quux"], options=["foo", "bar", "baz", "quux"])
	p = Bar(row, values='impressions', label='bins_cpm', xlabel = 'eCPM_bin', ylabel = 'Impressions',stack='sales_channel',agg='sum',legend="top_right",title="Bokeh: eCPM_data", plot_width=800)
		
	yaxis = p.select( dict(type=Axis, layout="left"))[0]
	yaxis.formatter = NumeralTickFormatter(format="0,0")
	yaxis.ticker = SingleIntervalTicker(interval=2500000, num_minor_ticks=10)
	xaxis = p.select(dict(type=Axis, layout="below"))[0]
	xaxis.formatter = NumeralTickFormatter(format="$0.00")
       
	


##        source = ColumnDataSource(row)
##        columns = [
##                TableColumn(field="date", title="Dates", formatter=DateFormatter()),
##                TableColumn(field="cpm", title="cpm"),
##                TableColumn(field="impressions", title="Impressions"),
##                TableColumn(field="sales_channel", title="Sales_channel"),
##                TableColumn(field="bins_cpm", title="bins_cpm")
##                ]
##        data_table = DataTable(source=source, columns=columns, width=400, height=280)
        figJS,figDiv = components(p, CDN)
        return(render_template('figures.html',
                               figJS=figJS,
                               figDiv=figDiv,
                               titles = ['impressions','cpm & sales_channel'],
							   
                               tables=[row.to_html(classes='impressions')]
                               ))  
							   

if __name__ == "__main__":
    app.run(debug=True)

####        output_file("figures.html")
####        show(vform(data_table))
####		output_file("multi_select.html")
####		show(vform(multi_select))
