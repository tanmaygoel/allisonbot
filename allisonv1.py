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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
fav_artist = 'Frank Ocean'

r = sr.Recognizer()



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
			if 'Alison' in userinput:
				print("You said - " + userinput)
				break
		except sr.UnknownValueError:
			print("Waiting for " + name)
			#say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
			#engine.runAndWait()
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

def play(video):
	driver = webdriver.Chrome('/Users/tanmaygoel/Documents/GitHub/allisonbot/chromedriver') 
	driver.maximize_window()

	wait = WebDriverWait(driver, 3)
	presence = EC.presence_of_element_located
	visible = EC.visibility_of_element_located

	# Navigate to url with video being appended to search_query
	driver.get("https://www.youtube.com/results?search_query=" + str(video))

	# play the video
	wait.until(visible((By.ID, "video-title")))
	driver.find_element_by_id("video-title").click()

	wait_and_listen()
	os.system("killall -9 'Google Chrome'")
	
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

def get_custom_song_df(var, song_df):
	custom_song_df = song_df.loc[song_df['artist_name'] == var]
	custom_song_df = custom_song_df.drop_duplicates()
	return custom_song_df

def get_popular_song(custom_song_df):
	custom_song_df.sort_values(by='popularity', ascending = False) 
	fav = custom_song_df.iloc[0,2]
	return fav

def get_fav_genre(custom_song_df):
	genre = custom_song_df.iloc[0,0]
	return genre


def get_recs(genre, song_df):
	custom_song_df2 = song_df.loc[song_df['genre'] == genre]
	custom_song_df2 = custom_song_df2.sample(n=5)
	recommended_list = custom_song_df2.sort_values(by='valence', ascending = True)
	custom_song_df2.sort_values(by='valence', ascending = True)
	recommended = recommended_list[['artist_name', 'track_name', 'valence']]

	print(recommended)

	return recommended

###############################################################################
#First Contact
def intro():
	say("Hello there. What's your name?")
	name = listen()

	say("You said " + name + ". Did I hear that right?")
	reply = listen()

	x = is_in_affirm_list(reply)

	if x != "yes":
		# say("I'm sorry. Do you mind typing it for me?")

		# name = input("Enter your name - ")
		name = get_input('name')


def block_1():
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
		say("Enjoy the song! Just pause the song and call my name when you are done!")
		play("Happy Pharrell")

	elif current_sentiment == 'negative':
		say("Aw, I'm sorry to hear that, " + name + ". Here is a tune I like listening to when I am a bit sad.")
		say("Enjoy the song! Just pause the song and call my name when you are done!")
		play("I like me better Lauv")

	else:
		say("I am happy to make a new friend in you, "+ name + ". Here is my current favourite song!")
		say("Enjoy the song! Just pause the song and call my name when you are done!")
		play("Havana Camilla Cabello")

	
	#wait_and_listen()
	song_feedback1()

###############################################################################
#Second contact
def song_feedback1():

	say("Welcome back! So. Did you like that song?")

	reply = listen()

	x = is_in_affirm_list(reply)

	if x == "yes":
		say("I'm happy to hear that! I will play more such songs that you like.")

	elif x == "no":
		say("Oh, okay! No worries. Maybe I'll find a better song next time.")
	
	else:
		say("Thank you for telling me how you feel " + name + ".")

def song_feedback2():
	os.system("killall -9 'Google Chrome'")

	say("Hello again! How did that song make you feel?")

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

	say("Thank you for telling me your feelings " + name + ". Currently I sense " + current_tone + " in your words.")

###############################################################################
#Favourite artist
def block_2(song_df):
	say("Why don't you tell me your favorite artist at the moment?")
	fav_artist = listen().title()


	# say("You said " + fav_artist + ". Did I hear that right?")
	# reply = listen()

	# x = is_in_affirm_list(reply)

	# if x != "yes":
	# 	# say("I'm sorry. Do you mind typing it for me?")

	# 	# name = input("Enter your name - ")
	# 	fav_artist = get_input('artist')

	custom_df = get_custom_song_df(fav_artist, song_df)
	song = get_popular_song(custom_df)
	
	#say('I love ' + fav_artist + '! Im sure you have heard ' + song '! Its pretty popular')
	say("I love listening to " + fav_artist + "! Lets listen to "+ song + " together. Its my favourite song. Like last time, just pause the song and call my name when you are done!")

	#say("Here is " + x['song'].values[0].title() + " from " + x['movie'].values[0].title() + ".")
	#say("")
	play(fav_artist + " " + song)

	song_feedback2()

	say("Now that I have a better understanding of your music taste, I am compiling some songs that you may like and will help you improve your mood. Are you ready?")
	reply = listen()
	x = is_in_affirm_list(reply)
	
	if x != "yes":
		say("No worries. It was nice talking to you " + name + "! Hope to see you again!")

def block_3(song_df):
	custom_df = get_custom_song_df(fav_artist, song_df)
	recommended = get_recs(get_fav_genre(custom_df), song_df)

	say("Great! Let's begin")



#MAIN
print("Loading Allison...")
song_df = pd.read_excel('SpotifyFeatures.xlsx')
start = ''
start = input("\nAllison has been loaded. Input start - ")

if start != '':
	pass

#intro()
#block_1()
block_2(song_df)
block_3(song_df)