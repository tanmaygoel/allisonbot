from __future__ import print_function
import json
import os
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
import threading
import speech_recognition as sr
import wave

# If service instance provides API key authentication
# service = SpeechToTextV1(
#     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
#     url='https://stream.watsonplatform.net/speech-to-text/api',
#     iam_apikey='your_apikey')

service = SpeechToTextV1(
    iam_apikey='SDz0zh59o0CvGcDFWyHtody003oTTHUvm2cK63YOSiMk',
    url='https://gateway-tok.watsonplatform.net/speech-to-text/api'
)

#models = service.list_models().get_result()
#print(json.dumps(models, indent=2))

model = service.get_model('en-US_BroadbandModel')
#print(json.dumps(model, indent=2))

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

myRecognizeCallback = MyRecognizeCallback()

def stt():
    with open(join(dirname(__file__), './.', 'audio-file2.flac'),'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        service.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/flac',
            recognize_callback=myRecognizeCallback,
            model='en-US_BroadbandModel',
            #keywords=['colorado', 'tornado', 'tornadoes'],
            #keywords_threshold=0.5,
            #max_alternatives=3)
        )

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

wave.open('test.wav', 'wb')
wave.Wave_write.writeframes(data)
wave.Wave_write.close()


