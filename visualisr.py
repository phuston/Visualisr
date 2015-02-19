import pyglet
import time
import random
import alsaaudio
import audioop
from pyglet.window import key

window = pyglet.window.Window(fullscreen=True) #Instantiates pyglet window object

def update_image(dt):
	""" This function takes in a refresh rate in Hz, and performs
	the operations inside. Based on the current sound levels read
	from the alsaaudio PCM object, it selects the correct frame 
	from the working directory, and displays it.
	"""

	# Takes in audio sample from alsaaudio PCM object, read in at the specified rate of 8000 Hz.
	# This value is then remapped to [0, num_frames] to be able to select the appropriate frame
	l,data = inp.read()
	if l:
		# print audioop.rms(data,2)
		index = ((roundint(audioop.rms(data,2), max_volume, num_frames))/(max_volume/num_frames))
		# Error handling to prevent attempts to load nonexistent images
		if index > num_frames-1:
			index = num_frames-1

	img = imgs[index] 
	sprite.image = img
	sprite.scale = get_scale(window, img)
	sprite.x = 0
	sprite.y = 0
	window.clear() #Calling window.clear prompts the @window.event method on_draw() which draws the current sprite


@window.event
def on_draw():
	sprite.draw()

def get_scale(window, image):
	""" This function takes in the window and the image to be drawn
	and determines the correct size 

	"""
	if image.width > image.height:
		scale = float(window.width) / image.width
	else:
		scale = float(window.height) / image.height
	return scale

def roundint(val, max_volume, num_frames):
	""" Returns current volume level rounded to nearest frame available 
	Finds correct filename for frames that exist and
	correspond most closely to the current volume level """

	return int((max_volume/num_frames) * round(float(val)/(max_volume/num_frames)))


if __name__ == '__main__':

	max_volume = 25000
	num_frames = 100

	# Preload all images, create sprites from working directory to speed up render time
	imgs = [pyglet.image.load('FaceVisualisr/Visualize2/frame-%d.jpg' % i) for i in range(num_frames)]
	sprites = [pyglet.sprite.Sprite(img) for img in imgs]

	# Instantiate first sprite object
	img = imgs[0]
	sprite = pyglet.sprite.Sprite(img)
	sprite.scale = get_scale(window, img) 

	# Instantiation of alsaaudio PCM object for audio monitoring
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
	inp.setchannels(1)
	inp.setrate(8000) # Sets sampling rate to 8000 Hz
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(160)

	# Sets pyglet clock schedule to sync up with audio sampling rate
	pyglet.clock.schedule_interval(update_image, 1/8000.0)

	pyglet.app.run()