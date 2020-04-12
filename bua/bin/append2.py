#%%
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

file = '/Users/manuiglesias/Desktop/poc_bua/bua/bin/buadata.xlsx'
output = 'output_buadata.csv'
#%%
engine = create_engine('sqlite:///bua.db', echo=False)

#engine = create_engine('sqlite://', echo=False)

#%%
df = pd.read_csv(file, usecols=range(0, 8))

#%%
df.to_sql('Task', engine, if_exists='append', index=False )
#df2.to_sql('sw_role', engine, if_exists='replace', index=False )

results = engine.execute("Select * from task where activity='Processing - Inventory'")

final=pd.DataFrame(results, columns=df.columns)
final.to_excel(output, index=False)