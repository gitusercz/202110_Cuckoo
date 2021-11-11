#!/usr/bin/env python 

# This program is to simulate a cuckoo-clock
# In subfolder Sounds there are multiple folders. This script checks every minute if there is an associated folder
# in Sounds. If there is a folder it plays whatever mp3 it finds there. 
# There should be one wav or mp3 file in that folder, name does not matter as long as it does not have any spaces in the name

# Program relies on mpg123 to be installed: 
#	sudo apt-get install mpg123


#	The & tells the shell to run the command in the background. This way you can actually play more than one file at once.
#	The -q option to mpg123 suppresses diagnostic messages. You can remove it if you'd like to see song titles.
#	The sleep(0.1) call is necessary to avoid spawning tons of mpg123 calls from a single button press.
 
import sys, termios, tty, os, time, datetime
from time import strftime
from datetime import datetime

print("Cuckoo clock has started, waiting for all services to start..")
time.sleep(10)
print("Ok, ready! \n")
 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def logfileupdater(logfileupdater_logfile_fullpath,logfileupdater_message_tobelogged):
	if os.path.isfile(logfileupdater_logfile_fullpath) == False:
		logfile = open(logfileupdater_logfile_fullpath,"w")
		logfile.write("This is a logfile for Cuckoo-clock. Records all events with timestamps. \n\nTimestamp,Event\n") 
		logfile.close()
	else:
		with open(logfileupdater_logfile_fullpath,"a") as log:
			log.write("\n"+strftime("%Y-%m-%d %H:%M:%S")+","+logfileupdater_message_tobelogged)

def pressedcharacter_handler(pressedcharacter_handler_capturedchar):
	currentchar = pressedcharacter_handler_capturedchar
	print(currentchar + " is the time")
        if os.path.isdir(leadingpath + '/Sounds/'+currentchar+'/') == True:
	        print(currentchar + " has an associated sound to play! ")
		for root, dirs, files in os.walk(leadingpath + '/Sounds/'+currentchar+'/'):
			for file in files:
				if file.endswith(".mp3"):
					finalpath = os.path.join(root, file)
					logfileupdater(local_log_file_fullpath,currentchar + " pressed. Playing: "+ finalpath)
		logfileupdater(local_log_file_fullpath,currentchar + " is the time.")
		os.system('mpg123 -q '+ finalpath +' &')
		
	else:
		print(currentchar + " does not have an associated folder! ")
	


	
 
check_frequency = 60		# needed for debouncing and spawning a lot of os.system calls. 
leadingpath, runningfile = os.path.split(os.path.realpath(__file__))   # splitting /home/pi/dev/run.py to /home/pi/dev  AND run.py 
#With thios method the folder, where the script is can be querried. This makes the python script portable. 
local_log_file_fullpath = leadingpath + '/CuckooLog.txt'

#logging to the logfile
with open(local_log_file_fullpath,"a") as log:
			log.write("\n\n"+strftime("%Y-%m-%d %H:%M:%S")+","+"Started")
 
while True:
    now = datetime.now()
    timeStr = now.strftime("%H%M")
    print (timeStr)
    pressedcharacter_handler(timeStr)
    time.sleep(check_frequency)
    
