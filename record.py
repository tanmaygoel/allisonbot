import webbrowser
import pyttsx3
import speech_recognition as sr
from watson_developer_cloud import TextToSpeechV1
import time
import pyglet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import random
import pandas as pd
import wave
import contextlib
from pydub import AudioSegment
from pydub.playback import play

r = sr.Recognizer()


with sr.Microphone() as source:
	print("Say something!")
	audio = r.listen(source)
	#r.adjust_for_ambient_noise(source, duration = 1)
	with open("output.wav", "wb") as f:
		f.write(audio.get_wav_data())
	
	try:
		userinput = r.recognize_google(audio)
		print("You said - " + userinput)
	except sr.UnknownValueError:
		#print("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
		say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))


fname = 'output.wav'
with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print(duration)

if duration < 3:
	audio_in_file = "output.wav"
	#audio_out_file = "out_sine.wav"
	sec = 3-duration+0.1
	print(sec)
	# create 1 sec of silence audio segment
	segment = AudioSegment.silent(duration=sec*1000)  #duration in milliseconds

	#read wav file to an audio segment
	song = AudioSegment.from_wav(audio_in_file)

	#Add above two audio segments    
	final_song = song + segment

	#Either save modified audio
	final_song.export('output.wav', format="wav")

with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print(duration)