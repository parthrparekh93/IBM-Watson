import json
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
  message_input={'text': 'Where is the lecture?'},
  context=context
)

print(json.dumps(response, indent=2))
