from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings

from flask import *
import pandas as pd
app = Flask(__name__)
@app.route('/')
@app.route("/tables")
def show_tables():

	db = create_engine(URL(**settings.DATABASE))
	#db.echo = False  # Try changing this to True and see what happens
	row=pd.read_sql_query('select * from "Sports_livesum"',con=db)
	return render_template('view.html',tables=[row.to_html(classes='sport')],titles = ['date','sport'])

if __name__ == "__main__":
    app.run(debug=True)
