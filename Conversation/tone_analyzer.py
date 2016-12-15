import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
   username='4998e736-6da5-4ac4-ae43-a34c0a603d6e',
   password='32smz86vQzde',
   version='2016-05-19')

def get_anger(s):
    response = tone_analyzer.tone(text=s, tones="emotion", sentences=False)
    #print response["document_tone"]["tone_categories"][0]["tones"][0]["tone_name"]
    return response["document_tone"]["tone_categories"][0]["tones"][0]["score"]
