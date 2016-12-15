import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
   username='4998e736-6da5-4ac4-ae43-a34c0a603d6e',
   password='32smz86vQzde',
   version='2016-05-19')
   
print(json.dumps(tone_analyzer.tone(text='A word is dead when it is said, some say. Emily Dickinson'), indent=2))
