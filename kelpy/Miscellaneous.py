# -*- coding: utf-8 -*-
"""
	Some miscellaneous useful functions
	
"""
import os
import sys
import random
import pygame
from time import time
from pygame.locals import *


## Some global variables we care about
screen, clock, WINDOW_WIDTH, WINDOW_HEIGHT = [None]*4

OFFSCREEN = [-10000, -10000]

Infinity = float("inf")

tab = '\t'
background_color = (255,255,255)

SPACEBAR_CHANGE_EVENT = pygame.USEREVENT + 0x1 # called by our main loop when space bar changes state (pressed to unpressed, etc)
def is_space_pressed(): return pygame.key.get_pressed()[K_SPACE]
SPACEBAR_NOHOLD_EVENT = pygame.USEREVENT + 0x2 # called by our main loop whenever the spacebar is NOT held down
NULL_EVENT            = pygame.USEREVENT + 0x3

ZONE_EVENT            = pygame.USEREVENT + 0x4

EXIT_KELPY_STANDARD_EVENT_LOOP            = pygame.USEREVENT + 0x5 # this event is for exiting loops, after completing some queue event

#pygame.mixer.pre_init(44100,-16,2, 1024 * 3) # sometimes we get scratchy sound -- use this from http://archives.seul.org/pygame/users/Oct-2003/msg00076.html
def ifelse(x,y,z):
	if x: return y
	else: return z
	
	
def q(x): return "\""+str(x)+"\""

def die(x):
	print  >>sys.stderr, x
	quit()
	
def flip(): return (random.random() < 0.5);

def kstimulus(*args):
	"""
		Returns the stimulus for a path f (relative to the kelpy stimulus file)
	"""
	
	f = os.path.dirname( __file__ )+"/stimuli/"
	
	if len(args) == 1: f = f+args[0]
	else:              
		for a in args:
			#print "A=",a, a[1], a[1] == '.', f[-1] != '/' and a[1] != '.' and a[1] != '/'
			if f[-1] != '/' and a[0] != '.' and a[0] != '/': f = f+"_"+a # don't append when we ar a slash or an extension
			else:            f = f+a
	
	return f

def next_alphabetical(s):
	"""
		Returns the next string in alphabetical order ( "aab" -> "aac", etc)
		From http://stackoverflow.com/questions/932506/how-can-i-get-the-next-string-in-alphanumeric-ordering-in-python
	"""
	strip_zs = s.rstrip('z')
	if strip_zs: return strip_zs[:-1] + chr(ord(strip_zs[-1]) + 1) + 'a' * (len(s) - len(strip_zs))
	else: return 'a' * (len(s) + 1)

	
blankcursor_strings = (               #sized 24x24
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ")
blank_cursor=pygame.cursors.compile(blankcursor_strings, black='X', white='.', xor='o')

def xor(x,y): return (x and (not y)) or ( (not x) and y )

def sample1(*args): return sample_one(*args)
def sample_one(*args): 
	if len(args) == 1: return random.sample(args[0],1)[0] # use the list you were given
	else:             return random.sample(args, 1)[0]   # treat the arguments as a list

def loop_till_key(key=K_RETURN):
	
	while True:
		if pygame.key.get_pressed()[key] == 1: return
		
		for event in pygame.event.get():
				if event.type == QUIT: quit()
				if event.type == KEYDOWN and event.key == K_ESCAPE: quit()


def play_sound(sound, wait=False, volume=0.5):
	#snd = pygame.mixer.Sound( sound )
	#snd.set_volume( volume )
	#snd.play()
					
	pygame.mixer.music.load(sound)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play()
	
	if wait:
		while pygame.mixer.music.get_busy(): pass
		
		
def initialize_kelpy(dimensions=(1024,768), bg=(250,250,250), fullscreen=False):
	"""
		Calls a bunch of pygame functions to set up the screen, etc. 
		- Fullscreen - if true, we override the dimensions
	"""
	
	global background_color # change the up-one-level variable
	background_color = bg
	
	pygame.init()
	
	if fullscreen: screen = pygame.display.set_mode( (0,0), pygame.FULLSCREEN)
	else:          screen = pygame.display.set_mode(dimensions)
	
	clock = pygame.time.Clock()
	
	## And load our icon
	icon = pygame.image.load(kstimulus("icons/icon_100x100.png"))
	pygame.display.set_icon(icon)
	pygame.display.set_caption("Kelpy")
	
	if not pygame.font: print 'Warning, fonts disabled'
	if not pygame.mixer: print 'Warning, sound disabled'
	
	return screen
	
def clear_screen(screen):
	screen.fill(background_color)
	pygame.display.flip()


def kely_standard_event_loop(screen, *args, **kwargs):
	"""
		This is a cute way to loop indefinitely (or until max time -- TODO implement this), while updating kelpy objects. 
		Here, each arg gets "update()" called on each loop, and we yeild the current time. 
		We also process the screen flips, etc. etc. 
		
		If a pygame event of type LOOP_EXIT_EVENT is thrown, then we exit this loop
	"""
	
	# Make events for when spacebar changes status
	old_is_space_pressed = is_space_pressed
	start_space_up = float("-inf")
	last_space_change_time = float("-inf")
	while True:
		pygame.display.flip() # display the previous cycle
		
		if kwargs.get('throw_spacebar_events', False):
			# handle space press events -- throw changes and throw all holds
			sp = is_space_pressed()
			if old_is_space_pressed != sp:
				t = time()
				pygame.event.post(pygame.event.Event(SPACEBAR_CHANGE_EVENT, is_space_pressed=sp, time_changed=(t-last_space_change_time)))
				old_is_space_pressed = sp
				last_space_change_time = t
				
				if not sp: start_space_up = t # record the time of space press starting
			if not sp: # post the spacebar hold event
				pygame.event.post(pygame.event.Event(SPACEBAR_NOHOLD_EVENT, time=(time()-start_space_up)))
		
		if kwargs.get('throw_null_events', False): # these will throw a "NULL" event every iteration, in order to process things outside this loop each time point
			pygame.event.post(pygame.event.Event(NULL_EVENT))
		
		# process all events
		for event in pygame.event.get():
			
			yield event # so we can handle EXIT, etc., outside, but don't have to
			
			if event.type == QUIT: quit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE: quit()
			elif event.type == EXIT_KELPY_STANDARD_EVENT_LOOP: return # we are done with this loop
			
		# fill the background and update everything
		screen.fill(background_color)
		for a in args:
			if isinstance(a, list): 
				for ai in a: ai.update()
			else: a.update() # love you, duck typing XXOO

			
			
			
			
			
			