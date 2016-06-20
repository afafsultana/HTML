from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


db = create_engine(URL(**settings.DATABASE))

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)
users = Table('Sports_livesum', metadata, autoload=True)
s = users.select()
rs = s.execute()

row = rs.fetchall()

print(row)
from flask_table import Table, Col
class ItemTable(Table):
  Date = Col('Date')
  sports = Col('sports')
  videocap = Col('videocap')
  

table = ItemTable(row)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template
