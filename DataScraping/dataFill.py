import psycopg2
#import urllib2
import json
from watson_developer_cloud import AlchemyLanguageV1
from bs4 import BeautifulSoup
import tone_analyzer

alchemy_language = AlchemyLanguageV1(api_key='b3425e39a3c407de56c9c08ca8854305db268925')

hostname = 'localhost'
username = 'postgres'
password = 'postgres'
database = 'columbiaconnect'

# Simple routine to run a query on a database and print the results:
def doQuery(conn) :
    cur = conn.cursor()
    pid = 1
    cid = 1
    pdic = {}
    cdic = {}
    with open('prof_course.txt','r') as f:
        for line in f:
            data_og = line.split('$')
            data = [i.strip() for i in data_og]
            #print data
            if(data[0] not in pdic):
                cur.execute("INSERT INTO professor2 VALUES (%s, %s, %s, %s, %s)",(pid,data[0],data[1],data[2],data[3]))
                pdic[data[0]]=pid
                pid+=1
            if(data[4] not in cdic):
                cur.execute("INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s)",(cid, data[4],data[5],data[1],data[6],""))
                cdic[data[4]] = cid
                cid+=1
            #cur.execute("INSERT INTO building VALUES (%s, %s, %s, %s)",(data[0],data[1],float(data[2]), float(data[3])))
    with open('prof_course.txt','r') as f:
        for line in f:
            data_og = line.split('$')
            data = [i.strip() for i in data_og]
            #print data
            cur.execute("INSERT INTO course_prof2 VALUES (%s, %s, %s, %s, %s, %s)",(cdic[data[4]], pdic[data[0]],data[7],data[8],data[9],data[10]))
    #put_reviews(cur, pdic, cdic)
'''
def put_reviews(cur, pdic, cdic):
    professors = ["http://culpa.info/professors/2742", "http://culpa.info/professors/4500", "http://culpa.info/professors/2568", 
    "http://culpa.info/professors/13217", "http://culpa.info/professors/1442", "http://culpa.info/professors/13116", 
    "http://culpa.info/professors/375", "http://culpa.info/professors/3366", "http://culpa.info/professors/13076", 
    "http://culpa.info/professors/1724", "http://culpa.info/professors/2941", "http://www.culpa.info/professors/42",
    "http://www.culpa.info/professors/2427","http://www.culpa.info/professors/1637","http://www.culpa.info/professors/3509",
    "http://www.culpa.info/professors/4210","http://www.culpa.info/professors/3409","http://www.culpa.info/professors/13070",
    "http://www.culpa.info/professors/4205", "http://www.culpa.info/professors/12959","http://www.culpa.info/professors/515",
    "http://www.culpa.info/professors/39","http://www.culpa.info/professors/4057","http://www.culpa.info/professors/4221"];
    #professors = ["http://culpa.info/professors/375"];
    pids = [1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16 ,17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29]
    for j,professor in enumerate(professors):
    	page = urllib2.urlopen(professor)
    	soup = BeautifulSoup(page)
        pid = pids[j]

    	# print soup.prettify().encode('UTF-8')
    	# print soup.find('div', class_='professor').find('div', class_='box').find('h1').contents[0]
    	reviews_array = list()
    	reviewToCourse = dict()
    	professor_info = soup.find('div', class_='professor').find('div', class_='box')
    	professor_name = professor_info.find('h1').contents[0].strip()
    	#dept_name = professor_info.contents[5].find('a').string.strip()
    	course_name = professor_info.contents[7].find('a').string.strip()
    	reviews = soup.find_all('div', class_='review_content')

    	reviews2 = soup.find_all('div', class_='meta')

    	for review in reviews:
    		temp = ""
    		statements = review.contents
    		for statement in statements:
    			if statement.string is not None:
    				temp += statement.string
    		reviews_array.append(temp)

      	for i, review in enumerate(reviews2):
    		try:
    			reviewToCourse[reviews_array[i]] = review.contents[3].find('a').find('span',class_='course_name').string.strip()
    		except:
    			reviewToCourse[reviews_array[i]] = course_name

    	print professor_name
    	#print dept_name
    	# print course_name
    	# print reviews_array
    	# print len(reviews_array)
        sentiment_array = list()
        emotion_array = []
        language_array = []
        social_array = []

    	for review in reviews_array:
            emotion_array.append(tone_analyzer.get_emotions(review))
            language_array.append(tone_analyzer.get_language(review))
            social_array.append(tone_analyzer.get_social(review))
        	sentiment_array.append(json.dumps(alchemy_language.sentiment(text=review)["docSentiment"]["type"]))
        count = 0
        for i, review in enumerate(reviewToCourse):
            print reviewToCourse[review]
            if(reviewToCourse[review] in cdic):
                count += 1
                cid = cdic[reviewToCourse[review]]
                cur.execute("INSERT INTO course_review VALUES (%s, %s, %s, %s)",(cid, pid,review,sentiment_array[i]))
                #print cid, pid,review#,sentiment_array[i]
        print count

'''

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.commit()
myConnection.close()
