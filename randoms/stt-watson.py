from watson_developer_cloud import TextToSpeechV1
import json

text_to_speech = TextToSpeechV1(
    iam_apikey='xn6ssmk4zrDESReJqnB34vMyTyDLtVT8XbkD4Oag-D_T',
    url='https://gateway-tok.watsonplatform.net/text-to-speech/api'
)

with open('hello_world.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            'Hello world',
            'audio/wav',
            'en-US_AllisonVoice'
        ).get_result().content)