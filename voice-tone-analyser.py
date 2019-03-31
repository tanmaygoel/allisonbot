from deepaffects.realtime.util import chunk_generator_from_file, chunk_generator_from_url, get_deepaffects_client
import speech_recognition as sr
import wave
import contextlib
from pydub import AudioSegment
from pydub.playback import play
from os import system, name 
import json

r = sr.Recognizer()

TIMEOUT_SECONDS = 2000
apikey = "S9r61wIVfOA9lrq4lhFnDN284s0KVIyc"

# Set file_path as local file path or audio stream or youtube url
file_path = "output.wav"

# Set is_youtube_url True while streaming from youtube url
is_youtube_url = False
languageCode = "en-Us"
sampleRate = "16000"
encoding = "wav"

# DeepAffects realtime Api client
client = get_deepaffects_client()

metadata = [
	('apikey', apikey),
	('encoding', encoding),
	('samplerate', sampleRate),
	('languagecode', languageCode)
]
#emotion = {}

"""Generator Function

chunk_generator_from_file is the Sample implementation for generator funcion which reads audio from a file and splits it into
base64 encoded audio segment of more than 3 sec
and yields SegmentChunk object using segment_chunk

"""

# from deepaffects.realtime.types import segment_chunk
# segment_chunk(Args)

"""segment_chunk.

Args:
	encoding : Audio Encoding,
	languageCode: language code ,
	sampleRate: sample rate of audio ,
	content: base64 encoded audio,
	segmentOffset: offset of the segment in complete audio stream
"""

# Call client api function with generator and metadata
def get_tone_emotion():

	responses = client.IdentifyEmotion(
		# Use chunk_generator_from_file generator to stream from local file
		chunk_generator_from_file(file_path),
		# Use chunk_generator_from_url generator to stream from remote url or youtube with is_youtube_url set to true
		# chunk_generator_from_url(file_path, is_youtube_url=is_youtube_url),
		 TIMEOUT_SECONDS, metadata=metadata)

	# responses is the iterator for all the response values
	for response in responses:
		#print("Received message",response)
		emotion = str(response)
		break
		#print(type(x))
		
	print(emotion)
"""Response.
	response = {
		emotion: Emotion identified in the segment,
		start: start of the segment,
		end: end of the segment
	}
"""


def get_audio_duration():
	fname = 'output.wav'
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
	return duration

def increase_audio_duration(duration):
	audio_in_file = "output.wav"
	#audio_out_file = "out_sine.wav"
	sec = 3-duration+0.1

	# create silence audio segment
	segment = AudioSegment.silent(duration=sec*1000)  #duration in milliseconds

	#read wav file to an audio segment
	song = AudioSegment.from_wav(audio_in_file)

	#Add above two audio segments    
	final_song = song + segment

	#Either save modified audio
	final_song.export('output.wav', format="wav")

def listen():
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
			print("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
			#say("I'm sorry, I didn't quite get that. Why don't you try saying it again?")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

	duration = get_audio_duration()
	if duration < 3:
		increase_audio_duration(duration)

	get_tone_emotion()

listen()