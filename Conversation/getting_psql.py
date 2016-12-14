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

'''
#get time of oh
s = "SELECT pname, oh_time FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"
print doQuery(s)


#get time of lec
course = 'bayesian machine learning'
course = course.replace(" "," & ")
s = "SELECT name, cno, lec_time FROM course JOIN course_prof2 ON course.cid = course_prof2.cid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"
print doQuery(s)


#suggest course
concepts = ['learning','database']
courses = set()
for concept in concepts:
	s = "SELECT name, description FROM course where to_tsvector('english', name || ' ' || description) @@ to_tsquery('english', '" + concept + "')"
	res = doQuery(s)
	for i,j in res:
		courses.add(i)
print courses



#Intent = location, entity = professor_or_course, value = professor
print doQuery("SELECT pname, loc_no, loc_code, building.x_co, building.y_co FROM\
professor2 JOIN building ON professor2.loc_code = building.b_code where to_tsvector('english', pname) @@ to_tsquery('english', '%s')")
 
# Intent = location, entity = professor_or_course, value = course
entity_value = "Bayesian Machine Learning".replace(" ", " & ")
print doQuery("SELECT course.cno, course.name, loc_no, loc_code, building.x_co, building.y_co FROM course_prof2 JOIN building ON course_prof2.loc_code = building.b_code JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', course.name) @@ to_tsquery('english', '%s')")
 
# Intent = reviews, entity = professor_or_course, value = professor
entity_value = "bellovin"
print doQuery("SELECT pname, review, sentiment FROM professor2 JOIN course_review ON professor2.pid=course_review.pid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')")
# print doQuery("SELECT count(*), sentiment FROM\
# professor2 JOIN course_review ON professor2.pid=course_review.pid where to_tsvector('english', pname) @@ to_tsquery('english', '" + entity_value + "') GROUP BY sentiment")
 
# Intent = reviews, entity = professor_or_course, value = course
entity_value = "Machine Learning".replace(" ", " & ")
print doQuery("SELECT name, sentiment, review FROM course JOIN course_review ON course.cid=course_review.cid where to_tsvector('english', name) @@ to_tsquery('english', '%s')")
'''