import json
from getting_psql import doQuery
from watson_developer_cloud import ConversationV1

conversation = ConversationV1(
  username='e2668e32-d4e4-48f9-8050-13a437a30ea4',
  password='HxIQNbLB67Fh',
  version='2016-09-20'
)

context = {}

workspace_id = '500fe656-514a-4ef0-ac20-6be33318f043'

response = conversation.message(
  workspace_id=workspace_id,
  message_input={'text': 'Where does david sit?'},
  context=context
)

indices = json.dumps(response["entities"][0]["location"])[1:-1].split(",")
text = json.dumps(response["input"]["text"])
entity_value = text[int(indices[0].strip())+1 : int(indices[1].strip())+1]

print doQuery("SELECT pname, loc_no, loc_code, building.x_co, building.y_co FROM\
 professor2 JOIN building ON professor2.loc_code = building.b_code where to_tsvector('english', pname) @@ to_tsquery('english', '" + entity_value + "')")
