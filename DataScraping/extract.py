import urllib2
import json
from watson_developer_cloud import AlchemyLanguageV1
from bs4 import BeautifulSoup

wiki = "http://www.culpa.info/professors/1636"
page = urllib2.urlopen(wiki)
soup = BeautifulSoup(page)

alchemy_language = AlchemyLanguageV1(api_key='b3425e39a3c407de56c9c08ca8854305db268925')

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

print (json.dumps(alchemy_language.sentiment(url='http://www.huffingtonpost.com/2010/06/22/iphone-4-review-the-worst_n_620714.html'), indent=2))