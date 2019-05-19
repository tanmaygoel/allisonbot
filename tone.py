import json
from ibm_watson import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='jAp3XAWT2awIhVzTmxg5WljgEzMfHbmteYFykmoj2iwv',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

text = 'I am very upset and sad with this behaviour'

tone_analysis = tone_analyzer.tone(
    {'text': text},
    content_type='text/html'
).get_result()

print(tone_analysis['document_tone']['tones'])