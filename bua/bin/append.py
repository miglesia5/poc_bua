from flask_sqlalchemy import SQLAlchemy
import pandas as pd


f = open(r"buadata.csv", "r")
fString = f.read()

fList = []
for line in fString.split('\n'):
    fList.append(line.split(','))

print(fList)

db = SQLAlchemy()

#%%
import pandas as pd

db = SQLAlchemy()

cursor = db.cursor()
df = pd.read_csv('data/book3.csv', usecols=range(0, 8))

print(df)

items = []

for i in df.itertuples():
     items.append((i[0],
                   i[1],
                   i[2],
                   i[3],
                   i[4],
                   i[5],
                   i[6],
                   i[7]))

len(items)
# #%%
sql = " insert into TASK (activity, " \
      "tool, " \
      "product, " \
      "summary, " \
      "avg_time, " \
      "volume, " \
      "pain_point, " \
      "pain_point_time)" \
      "values (?,?,?,?, ?, ?, ?, ?)"
#
cursor.executemany(sql, items)