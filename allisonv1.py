import webbrowser
import pyttsx3
import speech_recognition as sr
from textblob import TextBlob
import tkinter as tk 
from watson_developer_cloud import TextToSpeechV1
import json
import time
import pyglet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os


#Different word lists

text_to_speech = TextToSpeechV1(
    iam_apikey='D2ACR9YVIiMPFN_qzhtVkS2Fp9pWN4JDh8Dlf5cB99M0',
    url='https://stream.watsonplatform.net/text-to-speech/api'
)

yes_list = ["yes", "yep", "yup", "yeah", "ya", "yah"]
no_list = ["no", "nope", "nop", "nah", "not really"]
name = "tanny" #default

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# engine.setProperty('voice', voices[17].id)
analyser = SentimentIntensityAnalyzer()

r = sr.Recognizer()

def say(text_input):
	# print("Pybot - " + text + "\n")
	# engine.say(text)
	# engine.runAndWait()

	# tts = gTTS(text=text_input, lang='en')
	# tts.save("file.mp3")
	# os.system("mpg321 file.mp3")

	filename = "ibm-tts.wav"

	with open(filename, 'wb') as audio_file:
	    audio_file.write(
	        text_to_speech.synthesize(
	            text_input,
	            'audio/wav',
	            'en-US_AllisonV2Voice'
	        ).get_result().content)

	music = pyglet.media.load(filename, streaming=False)
	print("Allison - " + text_input + "\n")
	music.play()
	time.sleep(music.duration)
	

def listen():
	x = 1

	while x == 1:
		with sr.Microphone() as source:
		    print("Say something!")
		    audio = r.listen(source)
		    
		try:
			userinput = r.recognize_google(audio)
			print("You said - " + userinput)
			break
		except sr.UnknownValueError:
			print("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
			say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
		except sr.RequestError as e:
		    print("Could not request results from Google Speech Recognition service; {0}".format(e))

	return userinput

def wait_and_listen():
	x = 1

	while x == 1:
		with sr.Microphone() as source:
		    print("Say something!")
		    audio = r.listen(source)
		    
		try:
			userinput = r.recognize_google(audio)
			print("You said - " + userinput)
			break
		except sr.UnknownValueError:
			print("No value")
			#say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
			#engine.runAndWait()
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
	
def get_sentiment(text):
	# sent_text = TextBlob(text)

	# sentiment = sent_text.sentiment.polarity
	# #print(sentiment)
	# return sentiment
	score = analyser.polarity_scores(text)
	return score
	

def is_in_affirm_list(sentence):
	for word in yes_list:
		if word in sentence:
			return "yes"
	
	for word in no_list:
		if word in sentence:
			return "no"
		else:
			return 0

# def get_name():
# 	string = entry.get()
# 	#say("Awesome! Nice to meet you " + string + ". How are you doing today?")
# 	global root
# 	root.destroy()

# 	global name
# 	name = string


###############################################################################
#First Contact

say("Hello there. What's your name?")
reply = listen()

name = reply

say("You said " + name + ". Did I say that right?")
reply = listen()

x = is_in_affirm_list(reply)

if x != "yes":
	say("I'm sorry. Do you mind typing it for me?")

	name = input("Enter your name - ")
	
	# root = tk.Tk()
	
	# label = tk.Label(root, text = "Name")
	# label.grid(row = 0, column = 0)

	# entry = tk.Entry(root)
	# entry.grid(row = 0, column = 1)

	# button = tk.Button(root, text = 'Submit', command = get_name)
	# button.grid(row = 1, column = 1)

	# #root.mainloop()
	# #root.destroy()

say("Awesome! Nice to meet you " + name + ". How are you doing today?")

reply = listen()

sentiment = get_sentiment(reply)

if sentiment['compound'] >= 0.05:
	say("That's amazing " + name + ". Glad to hear that. Here is a song for you")
	webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")

elif sentiment['compound'] <= -0.05:
	say("That's okay" + name + "! The day is over now. Let me soothe you with some nice music")
	webbrowser.open("https://www.youtube.com/watch?v=xDhjma091uI")

else:
	say("Nothing good, but nothing bad either! "+ "Right " + name + "? Here is a song for you!")
	webbrowser.open("https://www.youtube.com/watch?v=HCjNJDNzw8Y")

say("Just pause the song and say hello to me when you are done listening!")
wait_and_listen()

###############################################################################
#Second contact
os.system("killall -9 'Google Chrome'")

say("So. Did you like that song?")

reply = listen()

x = is_in_affirm_list(reply)

if x == "yes":
	say("I'm happy to hear that! I will play more such songs that you like.")

else:
	say("Oh, that's a shame. I really liked it. But I will remember your preference.")

###############################################################################
#Favourite movie

say("Why don't you tell me your favorite movie?")
reply = listen()



