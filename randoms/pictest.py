import pyglet
import time
# pick an animated gif file you have in the working directory
ag_file = "graphics/talk.gif"

def showgif():
	
	animation = pyglet.resource.animation(ag_file)
	sprite = pyglet.sprite.Sprite(animation)
	# create a window and set it to the image size
	win = pyglet.window.Window(width=sprite.width, height=sprite.height)
	# set window background color = r, g, b, alpha
	# each value goes from 0.0 to 1.0
	green = 0, 1, 0, 1
	pyglet.gl.glClearColor(*green)
	@win.event
	def on_draw():
	    win.clear()
	    sprite.draw()
	pyglet.app.run()

	time.sleep(5)

	pyglet.app.exit()
	

showgif()
