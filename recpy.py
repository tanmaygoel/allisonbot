import pandas
import numpy as np


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

	return recommended


song_df = pandas.read_excel('SpotifyFeatures.xlsx')

var= input("Please tell me your favorite Artist ")
print("Playing a popular", var, "song")

custom_df = get_custom_song_df(var, song_df)

fav = get_popular_song(custom_df)
print("Now playing", fav)

recommended = get_recs(get_fav_genre(custom_df), song_df)

print(recommended)