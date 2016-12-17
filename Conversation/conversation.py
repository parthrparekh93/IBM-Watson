import json
from getting_psql import doQuery
from watson_developer_cloud import ConversationV1
import operator
import sys

text = ""

result_dict = {}

# print json.dumps(response,indent=2)
def get_loc(response):
	entities = response["entities"]
	oh_lec = 0
	for entity in entities:
		if entity["entity"] == "officehours_or_lecture":
			oh_lec = entity["value"]

	res = []
	found = False

	for entity in entities:
		if entity["entity"] == "professor" or entity["entity"] == "course":
			entity_value = entity["value"]
			entity_value = entity_value.replace(" ", " & ")

			if entity["entity"] == "professor":
				if oh_lec == 0 or oh_lec == "office hours":
					s = "SELECT pname, cno, name, professor2.loc_no, professor2.loc_code, building.x_co, building.y_co FROM professor2 JOIN building ON professor2.loc_code = building.b_code JOIN course_prof2 ON professor2.pid = course_prof2.pid JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT pname, cno, name, course_prof2.loc_no, course_prof2.loc_code, building.x_co, building.y_co FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid JOIN building ON course_prof2.loc_code = building.b_code JOIN course ON course_prof2.cid = course.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

			elif entity["entity"] == "course":
				if oh_lec == 0 or oh_lec == "lecture":
					s = "SELECT pname, cno, name, course_prof2.loc_no, course_prof2.loc_code, building.x_co, building.y_co FROM course_prof2 JOIN building ON course_prof2.loc_code = building.b_code JOIN course ON course.cid = course_prof2.cid JOIN professor2 ON course_prof2.pid = professor2.pid where to_tsvector('english', course.name) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT pname, cno, name, professor2.loc_no, professor2.loc_code, building.x_co, building.y_co FROM course_prof2 JOIN professor2 ON course_prof2.pid = professor2.pid JOIN building ON professor2.loc_code = building.b_code JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', course.name) @@ to_tsquery('english', '%s')"

			s = s.replace("%s",entity_value)
			val = doQuery(s)
			for v in val:
				tdic = {}
				tdic["professor"] = v[0]
				tdic["cno"] = v[1]
				tdic["coursename"] = v[2]
				tdic["loc_code"] = v[3]
				tdic["loc_name"] = v[4]
				tdic["x_coord"] = v[5]
				tdic["y_coord"] = v[6]
				found = True
				res.append(tdic)

	result_dict["found"] = found
	result_dict["value"] = res



def get_time(response):
	entities = response["entities"]
	oh_lec = 0
	for entity in entities:
		if entity["entity"] == "officehours_or_lecture":
			oh_lec = entity["value"]

	res = []
	found = False


	for entity in entities:
		if entity["entity"] == "professor" or entity["entity"] == "course":
			entity_value = entity["value"]
			entity_value = entity_value.replace(" ", " & ")

			if entity["entity"] == "professor":
				if oh_lec == 0 or oh_lec == "office hours":
					s = "SELECT pname, cno, name, oh_time FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

				else:
					s = "SELECT pname, cno, name, lec_time FROM professor2 JOIN course_prof2 ON professor2.pid = course_prof2.pid JOIN course ON course.cid = course_prof2.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"

			elif entity["entity"] == "course":
				if oh_lec == 0 or oh_lec == "lecture":
					s = "SELECT pname, cno, name, lec_time FROM course JOIN course_prof2 ON course.cid = course_prof2.cid JOIN professor2 ON professor2.pid = course_prof2.pid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"
				else:
					s = "SELECT pname, cno, name, oh_time FROM course JOIN course_prof2 ON course.cid = course_prof2.cid JOIN professor2 ON professor2.pid = course_prof2.pid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"

			s = s.replace("%s",entity_value)
			val = doQuery(s)
			for v in val:
				tdic = {}
				tdic["professor"] = v[0]
				tdic["cno"] = v[1]
				tdic["coursename"] = v[2]
				tdic["time"] = v[3]
				found = True
				res.append(tdic)

	result_dict["found"] = found
	result_dict["value"] = res


def get_reviews(response):
	entities =  response["entities"]
	res = []
	found = False

	for entity in entities:
		if entity["entity"] == "professor" or entity["entity"] == "course":
			entity_value = entity["value"]
			entity_value = entity_value.replace(" ", " & ")
			if entity["entity"] == "professor":
				s = "SELECT pname, name, review, sentiment FROM professor2 JOIN course_review ON professor2.pid=course_review.pid JOIN course ON course.cid=course_review.cid where to_tsvector('english', pname) @@ to_tsquery('english', '%s')"
			else:
				s = "SELECT pname, name, review, sentiment FROM course JOIN course_review ON course.cid=course_review.cid JOIN professor2 ON professor2.pid=course_review.pid where to_tsvector('english', name) @@ to_tsquery('english', '%s')"
			s = s.replace("%s",entity_value)
			print doQuery(s)
			val = doQuery(s)
			for v in val:
				tdic = {}
				tdic["professor"] = v[0]
				tdic["coursename"] = v[1]
				tdic["review"] = v[2]
				tdic["sentiment"] = v[3]
				found = True
				res.append(tdic)

	result_dict["found"] = found
	result_dict["value"] = res



def get_suggestion(response):
	entities =  response["entities"]
	courses = set()
	res = []
	found = False
	text = response["input"]["text"]

	for entity in entities:
		if entity["entity"] == "concepts":
			indices = entity["location"]
			entity_value = text[indices[0]: indices[1]]
			entity_value = entity_value.replace(" ", " & ")
			s = "SELECT name, description FROM course where to_tsvector('english', name || ' ' || description) @@ to_tsquery('english', '%s')"
			s = s.replace("%s",entity_value)
			result = doQuery(s)
			for i,j in result:
				courses.add(i)
	for course in courses:
		res.append({"course": course})
		found = True
	result_dict["found"] = found
	result_dict["value"] = res



def entry(inputText):
	conversation = ConversationV1(username='e2668e32-d4e4-48f9-8050-13a437a30ea4', password='HxIQNbLB67Fh', version='2016-09-20')
	context = {}
	workspace_id = '500fe656-514a-4ef0-ac20-6be33318f043'
	response = conversation.message(
	  workspace_id=workspace_id,
	  message_input={'text': inputText},
	  context=context,
	  alternate_intents=True
	)
	result_dict["response"] = response
	result_dict["intent"] = response["intents"][0]["intent"]

	if response["intents"][0]["intent"] == "get_location":
		get_loc(response)

	elif response["intents"][0]["intent"] == "get_time":
		get_time(response)

	elif response["intents"][0]["intent"] == "reviews":
		get_reviews(response)

	elif response["intents"][0]["intent"] == "suggest_course":
		get_suggestion(response)

	elif response["intents"][0]["intent"] == "hello":
		result_dict["value"] = [{"text":"Hi, How may I help you?"}]

	elif response["intents"][0]["intent"] == "goodbye":
		result_dict["value"] = [{"text":"Thank you. Have a great day!"}]
	return result_dict

#print entry("How is alfio")
