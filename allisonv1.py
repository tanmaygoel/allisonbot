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
from google.cloud import texttospeech
from ibm_watson import ToneAnalyzerV3


#Different word lists

text_to_speech = TextToSpeechV1(
	iam_apikey='xn6ssmk4zrDESReJqnB34vMyTyDLtVT8XbkD4Oag-D_T',
	url='https://gateway-tok.watsonplatform.net/text-to-speech/api'
)

tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	iam_apikey='jAp3XAWT2awIhVzTmxg5WljgEzMfHbmteYFykmoj2iwv',
	url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tanmaygoel/Documents/GitHub/allisonbot/creds/My First Project-540a707ac7a2.json"

#DEFAULTS AND INITIALISATIONS
yes_list = ["yes", "yep", "yup", "yeah", "ya", "yah", "sure", "right", "correct", "Yes"]
no_list = ["no", "na", "nope", "nop", "nah", "not really", "not sure", "wrong"]

sad_tone = ['sadness', 'anger', 'fear', 'tentative']
happy_tone = ['joy', 'confident']
neutral_tone = ['analytical']

name = "Adam" 
current_sentiment = 'neutral'
current_tone = 'none'
sub_tone = 'none'
fav_movie = 'star wars'
fav_artist = 'Queen'

r = sr.Recognizer()
df = pd.read_excel('music_database.xlsx')


def say(text_input):

	filename = "tts.mp3"

	with open(filename, 'wb') as audio_file:
		audio_file.write(
			text_to_speech.synthesize(
				text_input,
				'audio/wav',
				'en-US_AllisonV2Voice'
			).get_result().content)

	# client = texttospeech.TextToSpeechClient()

	# # Set the text input to be synthesized
	# synthesis_input = texttospeech.types.SynthesisInput(text=text_input)

	# # Build the voice request, select the language code ("en-US") and the ssml
	# # voice gender ("neutral")
	# voice = texttospeech.types.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL, name = 'en-US-Wavenet-F')

	# # Select the type of audio file you want returned
	# audio_config = texttospeech.types.AudioConfig(
	# 	audio_encoding=texttospeech.enums.AudioEncoding.MP3)

	# # Perform the text-to-speech request on the text input with the selected
	# # voice parameters and audio file type
	# response = client.synthesize_speech(synthesis_input, voice, audio_config)

	# # The response's audio_content is binary.
	# with open(filename, 'wb') as out:
	# 	# Write the response to the output file.
	# 	out.write(response.audio_content)

	music = pyglet.media.load(filename, streaming=False)
	print("Allison - " + text_input + "\n")
	music.play()
	time.sleep(music.duration)


def listen():
	#start = time.time()

	#userinput = input("Say - ")
	
	while True:
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)
			#r.adjust_for_ambient_noise(source, duration = 1)
			
		try:
			userinput = r.recognize_google(audio)
			print("You said - " + userinput)
			break
		except sr.UnknownValueError:
			#print("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
			say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

	# end = time.time()
	# print("\nTime taken for listen function = " + str(end-start) + " seconds")

	return userinput

def wait_and_listen():
	#r.adjust_for_ambient_noise(sr.Microphone(), duration = 1)
	#userinput = input("Say - ")
	while True:
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)
			
		try:
			userinput = r.recognize_google(audio)
			if userinput == 'hello':
				print("You said - " + userinput)
				break
		except sr.UnknownValueError:
			print("No value")
			#say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
			#engine.runAndWait()
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
	
def get_sentiment(text):
	
	analyser = SentimentIntensityAnalyzer()
	score = analyser.polarity_scores(text)
	return score

def get_sentiment_emotion(sentiment): 
	if sentiment['compound'] >= 0.05:
		x = 'positive'
	elif sentiment['compound'] <= -0.05:
		x = 'negative'
	else:
		x = 'neutral'
	return x

def get_sentiment_tone(text):
	
	#analyse the text to get tone
	tone_analysis = tone_analyzer.tone(
		{'text': text},
		content_type='text/html'
	).get_result()

	#how many tones did the api recognise?
	tone_len = len(tone_analysis['document_tone']['tones'])
	#print(tone_len)
	

	tone_list = []
	
	#loop to get the tones into list
	i = 0
	while i < tone_len:
		tone_list.append(tone_analysis['document_tone']['tones'][i]['tone_id'])
		i+=1

	return tone_list

	
def is_in_affirm_list(sentence):
	for word in yes_list:
		if word in sentence:
			return "yes"
	
	for word in no_list:
		if word in sentence:
			return "no"
		else:
			return 0

def get_input(value):

	sorry_list = ["I'm sorry.", "Oh, my bad!", "I'll definitely get it correct next time!"]

	say(random.choice(sorry_list) + " Do you mind typing it for me?")
	text_input = input("Enter " + value + " - ")
	return text_input


###############################################################################
#First Contact
def block_1():
	say("Hello there. What's your name?")
	name = listen()

	say("You said " + name + ". Did I hear that right?")
	reply = listen()

	x = is_in_affirm_list(reply)

	if x != "yes":
		# say("I'm sorry. Do you mind typing it for me?")

		# name = input("Enter your name - ")
		name = get_input('name')

	say("Awesome! Nice to meet you " + name + ". My name is Allison! How are you doing today?")

	reply = listen()

	current_sentiment = get_sentiment_emotion(get_sentiment(reply))
	print('\nCurrent Sentiment = ' + current_sentiment)
	
	tone_list = get_sentiment_tone(reply)
	if len(tone_list) != 0:
		global current_tone
		current_tone = tone_list[0]

	if len(tone_list) > 1:
		global sub_tone
		sub_tone = tone_list[1]

	print('Current Tone = ' + current_tone)
	print('Sub Tone = ' + sub_tone +'\n')

	if current_sentiment == 'positive':
		say("That's amazing " + name + ". I hope it only gets better! Here is a song that always makes me happy!")
		webbrowser.open("https://youtu.be/ZbZSe6N_BXs?t=28")

	elif current_sentiment == 'negative':
		say("Aw, I'm sorry to hear that, " + name + ". Here is a tune I like listening to when I am a bit sad.")
		webbrowser.open("https://www.youtube.com/watch?v=xDhjma091uI")

	else:
		say("I am happy to make a new friend in you, "+ name + ". Here is my current favourite song!")
		webbrowser.open("https://www.youtube.com/watch?v=HCjNJDNzw8Y")

	say("Just pause the song and say hello to me when you are done.")
	wait_and_listen()
	song_feedback1()

###############################################################################
#Second contact
def song_feedback1():
	os.system("killall -9 'Google Chrome'")

	say("So. Did you like that song?")

	reply = listen()

	x = is_in_affirm_list(reply)

	if x == "yes":
		say("I'm happy to hear that! I will play more such songs that you like.")

	elif x == "no":
		say("Oh, okay! No worries. Maybe I'll find a better song next time.")
	
	else:
		say("Interesting. I really enjoy talking to you " + name + "!")

def song_feedback2():
	os.system("killall -9 'Google Chrome'")

	say("So. How did that song make you feel?")

	reply = listen()

	current_sentiment = get_sentiment_emotion(get_sentiment(reply))
	print('\nCurrent Sentiment = ' + current_sentiment)
	
	tone_list = get_sentiment_tone(reply)
	if len(tone_list) != 0:
		global current_tone
		current_tone = tone_list[0]

	if len(tone_list) > 1:
		global sub_tone
		sub_tone = tone_list[1]

	print('Current Tone = ' + current_tone)
	print('Sub Tone = ' + sub_tone +'\n')

	if current_sentiment == 'positive':
		say("I can sense your mood is a little better now! Glad I could help.")

	elif current_sentiment == 'negative':
		say("It's okay " + name + ". Maybe the next song will do the trick!")

	else:
		say("Thank you for telling me how you feel " + name + ".")

###############################################################################
#Favourite movie
def block_2():
	say("Why don't you tell me your favorite artist at the moment?")
	fav_artist = listen()


	say("You said " + fav_movie + ". Did I hear that right?")
	reply = listen()

	x = is_in_affirm_list(reply)

	if x != "yes":
		# say("I'm sorry. Do you mind typing it for me?")

		# name = input("Enter your name - ")
		fav_movie = get_input('movie')

	x = df.loc[df['movie'] == fav_movie.lower()]
	x = x.sample(n=1)

	say(fav_movie + "! I love that movie! Here is my favourite track from " + fav_movie + ". " + x['song'].values[0].title() + ".")

	#say("Here is " + x['song'].values[0].title() + " from " + x['movie'].values[0].title() + ".")
	webbrowser.open(x['link'].values[0])
	say("Just pause the song and say hello to me when you are done.")

	wait_and_listen()
	song_feedback2()

#MAIN

#block_1()
block_2()