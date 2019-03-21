import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='ypJmU6pUYHMjIO-HaDiGom4hEKCayt4A2NRoGWFOcj2U',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

text = 'im not doing so good'

tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json'
).get_result()
print(json.dumps(tone_analysis, indent=2))