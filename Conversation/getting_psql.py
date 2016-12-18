import psycopg2

hostname = 'localhost'
# 'echo-01.db.elephantsql.com'
username = 'postgres'
# 'fkwmrwis'
password = 'postgres'
# 'MzWMfguQyEDEXHmlhwNue0WhmoHnA7z3'
database = 'columbiaconnect'
# 'fkwmrwis'

def doQuery(s) :
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = myConnection.cursor()
    cur.execute(s)
    return cur.fetchall()
    myConnection.commit()
    myConnection.close()

#print doQuery("Select * from professor2;")
