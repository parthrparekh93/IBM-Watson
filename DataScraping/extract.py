import urllib2
import json
from watson_developer_cloud import AlchemyLanguageV1
from bs4 import BeautifulSoup

alchemy_language = AlchemyLanguageV1(api_key='b3425e39a3c407de56c9c08ca8854305db268925')

#wiki = "http://www.culpa.info/professors/1636"
professors = ["http://www.culpa.info/professors/1636", "http://www.culpa.info/professors/1442", "http://www.culpa.info/professors/3366"];
for professor in professors:
	page = urllib2.urlopen(professor)
	soup = BeautifulSoup(page)

	# print soup.prettify().encode('UTF-8')
	# print soup.find('div', class_='professor').find('div', class_='box').find('h1').contents[0]
	reviews_array = list()
	professor_info = soup.find('div', class_='professor').find('div', class_='box')
	professor_name = professor_info.find('h1').contents[0].strip()
	dept_name = professor_info.contents[5].find('a').string.strip()
	course_name = professor_info.contents[7].find('a').string.strip()
	reviews = soup.find_all('div', class_='review_content')
	for review in reviews:
		temp = ""
		statements = review.contents
		for statement in statements:
			if statement.string is not None:
				temp += statement.string
		reviews_array.append(temp)

	print professor_name
	print dept_name
	print course_name
	# print reviews_array
	print len(reviews_array)

	for review in reviews_array:
		print (json.dumps(alchemy_language.sentiment(text=review)["docSentiment"]))
