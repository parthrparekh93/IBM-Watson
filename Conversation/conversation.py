import json
from getting_psql import doQuery
from tone_analyzer import get_anger
from watson_developer_cloud import ConversationV1
import operator

conversation = ConversationV1(
  username='e2668e32-d4e4-48f9-8050-13a437a30ea4',
  password='HxIQNbLB67Fh',
  version='2016-09-20'
)

context = {}

workspace_id = '500fe656-514a-4ef0-ac20-6be33318f043'

response = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': 'Where does ML lecture happen'},
  context=context
)

text = response["input"]["text"]

# print json.dumps(response,indent=2)

def get_loc(response):
	entities = response["entities"]
	oh_lec = 0
	for entity in entities:
		if entity["entity"] == "officehours_or_lecture":
			oh_lec = entity["value"]

	for entity in entities:
		if entity["entity"] == "professor" or entity["entity"] == "course":
			entity_value = entity["value"]
			entity_value = entity_value.replace(" ", " & ")

			if entity["entity"] == "professor":
				if oh_lec == 0 or oh_lec == "office hours":
					s = "SELECT pname, loc_no, loc_code, building.x_co, building.y_co FROM professor2 JOIN building ON professor2.loc_code = building.b_code where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT pname, cno, name, course_prof2.loc_no, course_prof2.loc_code, building.x_co, building.y_co FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid JOIN building ON course_prof2.loc_code = building.b_code JOIN course ON course_prof2.cid = course.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

			elif entity["entity"] == "course":
				if oh_lec == 0 or oh_lec == "lecture":
					s = "SELECT cno, name, loc_no, loc_code, building.x_co, building.y_co FROM course_prof2 JOIN building ON course_prof2.loc_code = building.b_code JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', course.name) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT cno, name, pname, professor2.loc_no, professor2.loc_code, building.x_co, building.y_co FROM course_prof2 JOIN professor2 ON course_prof2.pid = professor2.pid JOIN building ON professor2.loc_code = building.b_code JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', course.name) @@ to_tsquery('english', '%s')"
			s = s.replace("%s",entity_value)
			print doQuery(s)



def get_time(response):
	entities = response["entities"]
	oh_lec = 0
	for entity in entities:
		if entity["entity"] == "officehours_or_lecture":
			oh_lec = entity["value"]

	for entity in entities:
		if entity["entity"] == "professor" or entity["entity"] == "course":
			entity_value = entity["value"]
			entity_value = entity_value.replace(" ", " & ")

			if entity["entity"] == "professor":
				if oh_lec == 0 or oh_lec == "office hours":
					s = "SELECT pname, oh_time FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT pname, name, lec_time FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

			elif entity["entity"] == "course":
				if oh_lec == 0 or oh_lec == "lecture":
					s = "SELECT name, cno, lec_time FROM course JOIN course_prof2 ON course.cid = course_prof2.cid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT name, cno, pname, oh_time FROM course JOIN course_prof2 ON course.cid = course_prof2.cid JOIN professor2 ON professor2.pid = course_prof2.pid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"

			s = s.replace("%s",entity_value)
			print doQuery(s)


def get_reviews(response):
    entities =  response["entities"]
    for entity in entities:
        if entity["entity"] == "professor" or entity["entity"] == "course":
            entity_value = entity["value"]
            entity_value = entity_value.replace(" ", " & ")
            if entity["value"] == "professor":
                s = "SELECT pname, review, sentiment FROM professor2 JOIN course_review ON professor2.pid=course_review.pid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"
            else:
                s = "SELECT name, review, sentiment FROM course JOIN course_review ON course.cid=course_review.cid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"
            s = s.replace("%s",entity_value)
            reviews = doQuery(s)
            review_dict = {}
            for review in reviews:
                score = get_anger(review[1])
                review_dict[review] = score
            review_dict = sorted(review_dict.items(), key=operator.itemgetter(1))
            for i, j in review_dict:
                print i



def get_suggestion(response):
	entities =  response["entities"]
	courses = set()
	for entity in entities:
		if entity["entity"] == "concepts":
			indices = entity["location"]
			entity_value = text[indices[0]: indices[1]]
			entity_value = entity_value.replace(" ", " & ")
			print entity_value
			s = "SELECT name, description FROM course where to_tsvector('english', name || ' ' || description) @@ to_tsquery('english', '%s')"
			s = s.replace("%s",entity_value)
			res = doQuery(s)
			for i,j in res:
				courses.add(i)
	print courses


if response["intents"][0]["intent"] == "get_location":
	get_loc(response)

elif response["intents"][0]["intent"] == "get_time":
	get_time(response)

elif response["intents"][0]["intent"] == "reviews":
	get_reviews(response)

elif response["intents"][0]["intent"] == "suggest_course":
	get_suggestion(response)

elif response["intents"][0]["intent"] == "hello":
	print "Hi, How may I help you?"

elif response["intents"][0]["intent"] == "goodbye":
	print "Thank you. Have a great day!"
