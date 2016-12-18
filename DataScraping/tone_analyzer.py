import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
   username='4998e736-6da5-4ac4-ae43-a34c0a603d6e',
   password='32smz86vQzde',
   version='2016-05-19')

def get_tones(s):
    response = tone_analyzer.tone(text=s,  sentences=False)
    # print json.dumps(response["document_tone"]["tone_categories"], indent =2)
    emotions = response["document_tone"]["tone_categories"][0]["tones"]
    language = response["document_tone"]["tone_categories"][1]["tones"]
    emo_dic = {}
    lang_dic = {}
    # print emotions


    for e in emotions:
        # print e
        emo_dic[e["tone_id"]] = e["score"] 
    for e in language:
        lang_dic[e["tone_id"]] = e["score"] 
    return (emo_dic,lang_dic)

