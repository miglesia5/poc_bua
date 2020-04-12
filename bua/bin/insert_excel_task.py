#%%
from flask_sqlalchemy import SQLAlchemy

f = open(r"buadata.csv", "r")
fString = f.read()

fList = []
for line in fString.split('\n'):
    fList.append(line.split(','))

print(fList)
#%%
db = SQLAlchemy()


cursor = db.cursor()


rows = ""
for i in range(len(fList)-1):
    rows += "('{}','{}','{}','{}','{}','{}','{}','{}')".format(fList[i][0],
                                                               fList[i][1],
                                                               fList[i][2],
                                                               fList[i][3],
                                                               fList[i][4],
                                                               fList[i][5],
                                                               fList[i][6],
                                                               fList[i][7],
                                                               )




    if i != len(fList)-2:
        rows += ','

print(rows)
queryInsert = "INSERT INTO TASK VALUES"+ rows

try:
    cursor.execute(queryInsert)
    db.session.commit()
except:
    db.session.rollback()

db.session.close()
