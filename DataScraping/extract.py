import urllib2
from bs4 import BeautifulSoup

wiki = "http://www.culpa.info/professors/1636"
page = urllib2.urlopen(wiki)
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
print reviews_array	
print len(reviews_array)	