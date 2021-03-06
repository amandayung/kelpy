# -*- coding: utf-8 -*-
"""
	Construct a bunch of images of the pointy star objects

	find . -exec convert {} {}.jpg \;
"""

import Image

from math import atan2, cos, sin, sqrt
from random import random, choice

WIDTH = 600
HEIGHT = 600
WD2 = float(WIDTH/2)
HD2 = float(HEIGHT/2)
PI = 3.14159265358979323
PID2 = PI / 2.0
PIPI = 2.0 * PI

out_dir = "pinwheels/"

def make(angles, color=(50,50,50), BW=35, R=0.80, name="pin"):
	"""
		Make an N-spoked image
		
		BW = the width of a ball
		
		R = the radius of teh image (proportional to whole screen
		
	"""
	
	# set up the image
	im = Image.new('RGBA', (WIDTH, HEIGHT))
	pixels = im.load()
	for x in xrange(WIDTH): 
		for y in xrange(HEIGHT):
			pixels[x,y] = (255,255,255, 0) # set the colors
			
	# set up the "angles"
	angles.sort()
	angles.append( PIPI + angles[0]) # and loop around one bar so we can easily check modwise
	
	for x in xrange(WIDTH): 
		for y in xrange(HEIGHT):
			
			# convert to image-centered x,y, with -1,1 range
			
			xx = (x-WD2)/WD2
			yy = (y-HD2)/HD2
			
			# convert to polar coordinates
			theta = -atan2(yy,xx) # return negative--fixed below
			if theta < angles[0]: theta = theta + PIPI # translate this so it's right!
				
			r     = sqrt(xx*xx + yy*yy)
			
			# see if we are inside any of the angles
			for i in xrange(len(angles)-1):
				a = angles[i]
				b = angles[i+1]
				
				if (a < theta < b):
					
					## check if inside curve
					pct = (theta-a)/(b-a)
					if r <  R * 4.0 * (pct - 0.5) ** 2.0 or r < 0.2:
					#if r < pct or r < 0.2:
						pixels[x,y] = color
					
					break
			
			# see if this pixel is within BW of a point
			if BW > 0:
				for a in angles:
					bx = R*cos(a) * WD2 + WD2
					by = -R*sin(a) * HD2 + HD2
					
					if( (x-bx)**2 + (y-by)**2  < BW**2 ):
						pixels[x,y] = (255,0,0)
	
	im= im.resize((300,300), Image.ANTIALIAS) # downsize to antialias
	im.save(out_dir + "/" + name + ".png")
	


for i in xrange(10):
	
	angles = []
	for a in xrange(choice([2,3,4,5])):
		angles.append( random() * PIPI )
	
	make(angles, color=(50,50,50), BW=-1, name=str(i)+"_grey_nodots")
	make(angles, color=(50,50,50), name=str(i)+"_grey_dots")
	
	make(angles, color=(166,137,111), BW=-1, name=str(i)+"_brown_nodots")
	make(angles, color=(166,137,111), name=str(i)+"_brown_dots")
	
	make(angles, color=(113,166,111), BW=-1, name=str(i)+"_green_nodots")
	make(angles, color=(113,166,111), name=str(i)+"_green_dots")
	
	make(angles, color=(111,140,166), BW=-1, name=str(i)+"_blue_nodots")
	make(angles, color=(111,140,166), name=str(i)+"_blue_dots")
	
	make(angles, color=(164,111,166), BW=-1, name=str(i)+"_purple_nodots")
	make(angles, color=(164,111,166), name=str(i)+"_purple_dots")
	










