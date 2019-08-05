"""
Created on 02/07/2018
Author:Sangy Hanumasagar
GT ID: 902825462
"""


import numpy as np
from main import *

class shuttle_service:
	def __init__(self, busid, MaxWait):
		self.busid=busid
		self.MaxWait=MaxWait
		self.ToBoard_Que=[]
		self.Boarded_Grp=[]

		'''State Variables and global information'''
		self.Avg_Arr=.5 #3 passengers per minute 
		#[this means Avg_Arr number of people arrive per minute]

		# boolean variables: 1 if true, 0 if false
		self.AtHotel=1 #Bus available for passengers to board at hotel
		#BusFull=0 #Bus filled to capacity
		self.BusDepart=0 #Departing hotel to airport
		self.OnTrip=0 #Bus travelling to airport and back

		#variables for statistics
		self.Total_PBwait=0.0 #total Preboarding passenger waiting time
		self.Total_Bwait=0.0 #total passenger waiting time after boarding
		self.Total_Wait=0.0	#total passenger waiting time

		#variabes to track total passengers and total trips
		self.Tot_trips=0 #total number of trips of bus
		self.Tot_passengers=0 #total number of passengers ferried

		self.to=0	#left boundary of observation interval
		self.tf=300 #right boundary of observation interval
		self.passclock=0	#clock to maintain passenger arrivals
		self.busclock=0		#clock to track bus 
		self.clock=0	#main clock to monitor bus also
		self.BusStartWait=0
	
	'''Event Handlers: Bus and passenger Arrival, Boarding, Departure'''

	def eventhandler(self,func,timestamp):
		
		self.timestamp=timestamp
		if self.timestamp>self.tf and func=='PArr':
			print('Simulation Final Time Reached, No more passengers')
			return False
		elif func=='PArr':
			self.PassArrivals()
		elif func=='HBE':
			self.handle_boarding_event()
		elif func=='HDE':
			self.handle_departure_Event()
		elif func=='BArr':
			self.BusArrival()
		else:
			print('No such event:',func)

	
	def PassArrivals(self):	
		print('PASSENGER ARRIVAL EVENT @ ',self.passclock)
		#add customer to preboard waiting que
		self.Tot_passengers+=1 
		print('Tot pass:',self.Tot_passengers)

		self.clock=max(self.passclock,self.clock) #time is irreversible

		if self.AtHotel==1:	#if bus available, board the current passenger
			addEvent('HBE',self.passclock)
		
		self.ToBoard_Que.append(self.passclock) #timestamp of start of passenger preboard wait time
			
		#schedule next passenger arrival event
		self.passclock=self.passclock + np.random.exponential(1./self.Avg_Arr) 
		#3 customers per minute


		#if next pasenger is arriving later than Maxwait, depart at MaxWait
		if self.passclock>(self.BusStartWait+self.MaxWait) and len(self.Boarded_Grp)>0:
			self.clock=self.BusStartWait+self.MaxWait #update system clock
			addEvent('HDE',self.BusStartWait+self.MaxWait)

		elif self.timestamp>self.tf:
			addEvent('HDE',self.timestamp)

		addEvent('PArr',self.passclock)


	def handle_boarding_event(self):
		print('PASSENGER BOARDING EVENT @ ',self.timestamp)
		while len(self.ToBoard_Que)>0:
			self.pass_PBwait_End=self.timestamp
			self.Total_PBwait += (self.pass_PBwait_End-self.ToBoard_Que[0])
			#print('Total PBwait:',self.Total_PBwait)
			self.ToBoard_Que.pop(0)	#remove first passenger from to board que
			self.Boarded_Grp.append(self.timestamp)
			print('Len of boarded group',len(self.Boarded_Grp))
			print('Len of ToBoard_Que',len(self.ToBoard_Que))

			#Condition to check for departure
			if len(self.Boarded_Grp)==self.busid.size:
				pass_Bwait_End=self.timestamp
				for entry in self.Boarded_Grp:
					self.Total_Bwait += (pass_Bwait_End-entry)
				#print('Tot Boarded Wait',self.Total_Bwait)
				#schedule departure immediately
				addEvent('HDE',self.timestamp)
				break


	def handle_departure_Event(self):
		self.busclock=self.timestamp
		print('BUS DEPARTURE EVENT @ ',self.busclock)
		self.Tot_trips+=1
		self.AtHotel=0
		self.Boarded_Grp=[]
		self.busclock+= self.generate_commute()
		self.BusStartWait=10000
		addEvent('BArr',self.busclock)	
			
	def generate_commute(self): #for round trip from hotel to airport
		return np.random.uniform(self.busid.Trip_timeA,self.busid.Trip_timeB)

	def BusArrival(self):
		print('BUS ARRIVAL EVENT @ ',self.busclock)
		
		self.AtHotel=1
		self.BusStartWait=self.busclock
		if len(self.ToBoard_Que)>0:
			#print('Len of ToBoard_Que',len(self.ToBoard_Que))
			addEvent('HBE',self.busclock)


'''//// Simulation Constants; all time in minutes ////
Avg_Arr = mean passenger interarrival time (drawn from exponential distribution)

Bus Characterictics: 
	Size : capacity of bus
	Trip_time: travel time from hotel to airport and back
	Trip_timeA : lower limit of uniform distribution
	Trip_timeB : upper limit of uniform distribution
'''
class bus_prop:
	def __init__(self,size,Trip_timeA,Trip_timeB):
		self.size=size
		self.Trip_timeA=Trip_timeA
		self.Trip_timeB=Trip_timeB

#bus properties: capacity,trip time limits(lower and upper)
BusA=bus_prop(20,5,10)
BusB=bus_prop(40,15,20)

#variables for statistics
Avg_Wait=0.0 #average waiting time per passenger
Avg_pcent_occu=0.0 #average occupancy of bus over all trips

'''
###############INPUT ENTRIES: BUS CHOICE AND WAITING TIME####################
''' 
#Object of class Shuttle_Service
bus_wait_time=20
trial=shuttle_service(BusB,bus_wait_time)	#bus id and bus wait time

#Initiator of simulation
addEvent('PArr',0)
RunSim(trial)


print('total pass',trial.Tot_passengers)
print('total pass',trial.Total_PBwait,trial.Total_Bwait)
print('total trips',trial.Tot_trips)
