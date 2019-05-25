import os
import subprocess
import time

talk = '/Users/tanmaygoel/Documents/GitHub/allisonbot/graphics/talk.mp4'
listen = '/Users/tanmaygoel/Documents/GitHub/allisonbot/graphics/still.jpg'

def talkgif():
    subprocess.run(['open', talk], check=True)


talkgif()
#subprocess.run(['open', listen], check=True)




