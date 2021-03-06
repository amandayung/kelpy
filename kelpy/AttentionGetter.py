# -*- coding: utf-8 -*-
import types
import random
import GIFImage
import pygame
from pygame.locals import *
from time import time

#def play_reward_image(screen, g, duration=3.0):
#image = GIFImage.GIFImage(g)
def gif_attention_getter(screen, position, images, sounds=None, duration=None, keypress=None, stop_music=True, background_color=(255,255,255)):
	"""
		Plays a GIF and sound. If lists of these are given, a random one is chosen. 
		This can stop on a specified keypress or after a fixed duration
		If both are specified, we break on either. 
	"""
	# convert to lists if not
	if not isinstance(images, types.ListType): images = [images]
	if sounds is not None and not isinstance(sounds, types.ListType): sounds = [sounds]
		
	image = GIFImage.GIFImage(random.choice(images))
	
	if sounds is not None:
		pygame.mixer.music.load(random.choice(sounds))
		pygame.mixer.music.play()
	
	# record the time 
	start_time = time()
	
	# now loop until some exit criterion is met
	while True:
		# exit criteria
		if duration is not None and (time() - start_time) > duration: break
		if keypress is not None and pygame.key.get_pressed()[keypress] == 1: break
			
		# dspaly image
		screen.fill(background_color)
		image.render(screen, (position[0] - image.image.size[0]/2, position[1] - image.image.size[1]/2))
		pygame.display.flip()
		
		
		for event in pygame.event.get():
			if event.type == QUIT: quit()
			if event.type == KEYDOWN and event.key == K_ESCAPE: quit()
		
	if stop_music and sounds is not None:
		pygame.mixer.music.stop()
	
	return (time() - start_time) 
	

