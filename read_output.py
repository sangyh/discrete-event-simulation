'''this file reads the Sample_output text files and pulls numbers for  further analysis''' 
import matplotlib.pyplot as plt 
file=open("Sample_output-5.txt",mode= 'r')

Parrival_times=[]
Pboard_times=[]
busdep_times=[]
brdgrp_length=[] #length of boarded group
tobrdque_length=[] #length of to-board queue

for line in file.readlines():	#read sample output file line by line
	if line.startswith('PASSENGER ARRIVAL EVENT'):
		segments=line.split(' ')
		parr_time=float(segments[-1].rstrip()) #rstrip removes \n
		Parrival_times.append(parr_time) 


	if line.startswith('PASSENGER BOARDING EVENT'):
		segments=line.split(' ')
		pbrd_time=float(segments[-1].rstrip())
		Pboard_times.append(pbrd_time) 

	if line.startswith('BUS DEPARTURE EVENT'):
		segments=line.split(' ')
		bdep_time=float(segments[-1].rstrip())
		busdep_times.append(bdep_time) 

	if line.startswith('Len of boarded group'):
		segments=line.split(' ')
		bd_grp=int(segments[-1].rstrip())
		brdgrp_length.append(bd_grp)

	if line.startswith('Len of ToBoard_Que'):
		segments=line.split(' ')
		tobd_q=int(segments[-1].rstrip())
		tobrdque_length.append(tobd_q)

file.close()



#plt.plot(Parrival_times,range(len(Parrival_times)),label='Pass arrival')
#plt.plot(Pboard_times,range(len(Pboard_times)),'-o',label='Pass boarding')
#plt.plot(range(len(brdgrp_length)),brdgrp_length,'-o',label='Pass Boarded Grp')
plt.plot(range(len(tobrdque_length)),tobrdque_length,'o',label='Pass to board que')
plt.legend()
plt.show()
#print(tobrdque_length)