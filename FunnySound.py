#!/usr/bin/env python 

# This program is supposed to react to each keypress by playing a sound signal individually. 
# In subfolder Sounds there are multiple folders. Name of the folders are assigned to keypresses.
# There should be one wav or mp3 file in that folder, name does not matter as long as it does not have any spaces in the name

# Program relies on mpg123 to be installed: 
#	sudo apt-get install mpg123


#	The & tells the shell to run the command in the background. This way you can actually play more than one file at once.
#	The -q option to mpg123 suppresses diagnostic messages. You can remove it if you'd like to see song titles.
#	The sleep(0.1) call is necessary to avoid spawning tons of mpg123 calls from a single button press.
 
import sys, termios, tty, os, time
from time import strftime
from datetime import datetime

print("FunnySound has started, waiting for all services to start..")
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
		logfile.write("This is a logfile for FunnySound scripts. . Records all events with timestamps. \n\nTimestamp,Event\n") 
		logfile.close()
	else:
		with open(logfileupdater_logfile_fullpath,"a") as log:
			log.write("\n"+strftime("%Y-%m-%d %H:%M:%S")+","+logfileupdater_message_tobelogged)

def pressedcharacter_handler(pressedcharacter_handler_capturedchar):
	currentchar = pressedcharacter_handler_capturedchar
	print(currentchar + " pressed")
	for root, dirs, files in os.walk(leadingpath + '/Sounds/'+currentchar+'/'):
		for file in files:
			if file.endswith(".mp3"):
				finalpath = os.path.join(root, file)
	logfileupdater(local_log_file_fullpath,currentchar + " pressed. Playing: "+ finalpath)
	os.system('mpg123 -q '+ finalpath +' &')
	time.sleep(button_delay)
	


	
 
button_delay = 0.2		# needed for debouncing and spawning a lot of os.system calls. 
leadingpath, runningfile = os.path.split(os.path.realpath(__file__))   # splitting /home/pi/dev/run.py to /home/pi/dev  AND run.py 
#With thios method the folder, where the script is can be querried. This makes the python script portable. 
local_log_file_fullpath = leadingpath + '/FunnyLog.txt'

#logging to the logfile
with open(local_log_file_fullpath,"a") as log:
			log.write("\n\n"+strftime("%Y-%m-%d %H:%M:%S")+","+"Started")
 
while True:
    char = getch()
 
    if (char == "q"):
        print("Stop!")
        os.system('killall mpg123')
        logfileupdater(local_log_file_fullpath,"q pressed, exiting.")
        exit(0)
 
    elif (char == "w"):
        pressedcharacter_handler("w")
    elif (char == "e"):
        pressedcharacter_handler("e")
    elif (char == "r"):
        pressedcharacter_handler("r")
    elif (char == "t"):
        pressedcharacter_handler("t")
    elif (char == "z"):
        pressedcharacter_handler("z")
        
 
    elif (char == "1"):
        print("Number 1 pressed")
        time.sleep(button_delay)
