"""
Created on 2/05/2018
Author:Sangy Hanumasagar
GT ID: 902825462
"""

import operator

'''Define Data Structure for event list and event processor
Event: Tuple of (ID,timestamp)
Event List: List of events to be executed
'''

	
EventList=[]

def addEvent (event,time):	
	EventList.append((event,time))

def printEvent(data):
	for key,val in data:
		print(key,' ',val)

def getNextEvent():
	next_event=EventList[0]
	for item in EventList:
		if item[1]<next_event[1]:
			next_event=item
	return next_event

def RunSim(object):
	while EventList:
		curr_event=getNextEvent()
		EventList.pop(EventList.index(curr_event))
		object.eventhandler(curr_event[0],curr_event[1])
		print('Final event list:',EventList)
		print('----------------------------')

