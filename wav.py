#Final Project by Isaac Sleator (ics2106)

#=====================================================================[ MAIN METHOD ]====/
import os
import random
import time
from dsp import *
from sys import argv

#setting up optional location for output files
DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/"

print(DIRECTORY)

def getArgs(argv):
	if len(argv) < 3:
		print("Error: please enter 2 or more 8 or 16 bit .wav files as Command Line Argument")
		exit()	

#creating Wavefile objects
martin = Wavefile(argv[1])
jdilla = Wavefile(argv[2])
martinFrames = martin.frames
jdillaFrames = jdilla.frames

"""
#==================================TEST CASES============================================#
#1. copy file
martin.writeWav(DIRECTORY + '01_copy.wav', martinFrames)

#2. multiply volume by 0.3
quiet = martin.gain(0.3)						 			 
martin.writeWav(DIRECTORY + '02_quiet.wav', quiet)


#3. multiply volume by 10. Samples clip at maximum sample depth
loud = martin.gain(10)									
martin.writeWav(DIRECTORY + '03_loud.wav', loud)

#4. low pass filter file
filtered = martin.lowPassFilter()							
martin.writeWav(DIRECTORY + '04_filtered.wav', filtered)

#5. slow file to 0.8x speed
slowedDown = martin.changeSpeed(0.8)                       
martin.writeWav(DIRECTORY + '05_slowed.wav', slowedDown)

#6. speed file to double speed
spedUp = martin.changeSpeed(2)								
martin.writeWav(DIRECTORY + '06_doublespeed.wav', spedUp)

#7. negative speed = reversed 
negativeSpeed = martin.changeSpeed(-0.5)					
martin.writeWav(DIRECTORY + '07_negative0_5speed.wav', negativeSpeed)

#8. granulate file
granulated = martin.granulate(2500, 1000)					
martin.writeWav(DIRECTORY + '08_granulated.wav', granulated)

#9. granulate file, using optional speed arg. to slow it down
granulatedSlow = martin.granulate(10000, 3000, 0.8)		
martin.writeWav(DIRECTORY + '09_granulatedSlow.wav', granulatedSlow)

#10. chop file into 5000-sample chops (slices)
#reverse order of these chops and merge
choppedAudio = martin.chop(5000, martinFrames)             
reverseChop = martin.merge(list(reversed(choppedAudio)))   
martin.writeWav(DIRECTORY + '10_chopReverseMerge.wav', reverseChop)

#11. randomize order of these chops and merge
choppedAudio2 = martin.chop(14000, martinFrames)		   
random.shuffle(choppedAudio2)
reverseChop = martin.merge(choppedAudio2)   				
martin.writeWav(DIRECTORY + '11_chopRandomMerge.wav', reverseChop)

#12. reverse audio file, chop it, and write each chop to directory as wav file
reversed = martin.reverse()
chopReversed = martin.chop(20000, reversed)
martin.writeWav('12_revChop', chopReversed)


#13. adding two Wavefile objects together returns a new one
martindilla = martin + jdilla								
martindilla.writeWav(DIRECTORY + '13_martin+jdilla.wav')

#14. reversing the order of addition
dillamartin = jdilla + martin								
dillamartin.writeWav(DIRECTORY + '14_jdilla+martin.wav')


#15. making sure no samples were lost in addition ^^
try:
	assert dillamartin.nframes == jdilla.nframes + martin.nframes
except(AssertionError):
	print("addition failed [which it never should, but I need to add these features to my program]")
	exit()


#UNNECESSARY
#put all files in a playlist [and use dict and set for points on my project]
playlist = dict()

playlist['track1'] = DIRECTORY + '01_copy.wav'
playlist['track2'] = DIRECTORY + '02_quiet.wav'
playlist['track3'] = DIRECTORY + '03_loud.wav'
playlist['track4'] = DIRECTORY + '04_filtered.wav'
playlist['track5'] = DIRECTORY + '05_slowed.wav'
playlist['track6'] = DIRECTORY + '06_doublespeed.wav'
playlist['track7'] = DIRECTORY + '07_negative0_5speed.wav'
playlist['track8'] = DIRECTORY + '08_granulated.wav'
playlist['track9'] = DIRECTORY + '09_granulatedSlow.wav'
playlist['track10'] = DIRECTORY + '10_chopReverseMerge.wav'
playlist['track11'] = DIRECTORY + '11_chopRandomMerge.wav'
playlist['track13'] = DIRECTORY + '13_martin+jdilla.wav'
playlist['track14'] = DIRECTORY + '14_jdilla+martin.wav'



#play files in order using mplayer
try:
	play = True
	while(play):	
		for key in playlist:
			time.sleep(1)
			print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{}: ".format(playlist[key]))
			os.system('mplayer {}'.format(playlist[key]))
		play = False
except KeyboardInterrupt:
	print("we out")
	exit()