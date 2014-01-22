# -*- coding: utf-8 -*-
"""
	Some miscellaneous useful functions for eye tracking
	
"""

def looking_at_what(things):
	"""
	looking_at_what will return the object that is currently being looked at based on current eye gaze data.
	
	Keep in mind this function is not designed to handle looking at multiple objects, ie if there are two sprites on top of each other, it will return the first one in the ordered updates list.
	This may mean the item on the bottom will be returned first, if it is in line to be checked first.
	
	"""
	for x in iter(things, ):
		if x.is_looked_at():
			return x
	
	return None
	
def looking_proportions(things, trial_time):
	"""
	Based on the given trial_time, this function will determine the looking time proportionfor each object passed to it.
	The results are returned as a dictionary
	
	"""
	proportions = {}
	for x in iter(things, ):
		proportions[x] = x.get_look_time()/trial_time
		
	return proportions
	
def lookaway_time():
	"""
	Returns how long the screen has not been looked at for
	Should this be in normal miscellaneous instead under the kelpy loop? need clock...
	"""
	pass
