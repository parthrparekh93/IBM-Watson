import psycopg2

hostname = 'echo-01.db.elephantsql.com'
username = 'XXXX'
password = 'XXXX'
database = 'XXXX'

def doQuery(s) :
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = myConnection.cursor()
    cur.execute(s)
    return cur.fetchall()
    myConnection.commit()
    myConnection.close()

#print doQuery("Select * from professor2;")
