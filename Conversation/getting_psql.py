import psycopg2

hostname = 'echo-01.db.elephantsql.com'
username = 'fkwmrwis'
password = 'MzWMfguQyEDEXHmlhwNue0WhmoHnA7z3'
database = 'fkwmrwis'

def doQuery(s) :
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = myConnection.cursor()
    cur.execute(s)
    return cur.fetchall()
    myConnection.commit()
    myConnection.close()

#print doQuery("Select * from professor2;")
