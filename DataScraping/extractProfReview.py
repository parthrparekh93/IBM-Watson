import urllib2
import json
from watson_developer_cloud import AlchemyLanguageV1
from bs4 import BeautifulSoup

alchemy_language = AlchemyLanguageV1(api_key='b3425e39a3c407de56c9c08ca8854305db268925')

#wiki = "http://www.culpa.info/professors/1636"
professors = ["http://culpa.info/professors/2742", "http://culpa.info/professors/4500", "http://culpa.info/professors/2568", "http://culpa.info/professors/13217", "http://culpa.info/professors/1442", "http://culpa.info/professors/13116", "http://culpa.info/professors/375", "http://culpa.info/professors/3366", "http://culpa.info/professors/13076", "http://culpa.info/professors/1724", "http://culpa.info/professors/2941"];
#professors = ["http://culpa.info/professors/375"];
for professor in professors:
	page = urllib2.urlopen(professor)
	soup = BeautifulSoup(page)

	# print soup.prettify().encode('UTF-8')
	# print soup.find('div', class_='professor').find('div', class_='box').find('h1').contents[0]
	reviews_array = list()
	sentiment_array = list()
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
	print course_name
	# print reviews_array
	print len(reviews_array)

	# for review in reviews_array:
	# 	sentiment_array.append(json.dumps(alchemy_language.sentiment(text=review)["docSentiment"]["type"]))
