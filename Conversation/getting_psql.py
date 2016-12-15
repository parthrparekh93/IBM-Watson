import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'postgres'
database = 'columbiaconnect'

def doQuery(s) :
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = myConnection.cursor()
    cur.execute(s)
    return cur.fetchall()
    myConnection.commit()
    myConnection.close()
