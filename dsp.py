#dsp.py by Isaac Sleator [ics2106]
#WAVEFILE FUNCTIONS MODULE

import wave
import struct
import progressbar
import time
import math
import os
import copy
import tempfile
import re
from sys import argv

from logging import debug, info, warning, error, critical, basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL
basicConfig(level = DEBUG)

#==================================================================[ WAVEFILE CLASS ]====/
class Wavefile:

#------------------------------------------------------------------- read wav file ------/			
	def __init__(self, IN_FILE):
		
		if re.search("\.wav", IN_FILE):
			self.name = re.split('\.', IN_FILE)[0] #assign name without .wav
			wr = wave.open(IN_FILE, 'rb')
		else:
			error("please enter .wav file")
			exit()		
		
		self.filename = IN_FILE
		self.nchannels = wr.getnchannels()
		self.sampwidth = wr.getsampwidth()
		self.framerate = wr.getframerate()
		self.nframes = wr.getnframes()
		self.__comptype = wr.getcomptype()
		self.__compname = wr.getcompname()
		self.__data = wr.readframes(self.nframes)
		self.nsamples = self.nframes * self.nchannels
		wr.close()

	
		
		#CONVERTING BINARY FILE DATA TO USABLE LIST OF SAMPLES
		if self.sampwidth == 1:
			fmt = "%iB" % self.nsamples # read unsigned chars
			self.sampleDepth = 255
		elif self.sampwidth == 2:
			fmt = "%ih" % self.nsamples # read signed 2 byte shorts
			self.sampleDepth = 32767
		else:	
			raise ValueError("Only supports 8 and 16 bit audio formats.")
		intData = struct.unpack(fmt, self.__data)
		del self.__data #delete raw data to save space
		
		bar = progressbar.ProgressBar()
		print("importing wave file:")
		
		self.frames = [ [] for time in range(self.nchannels) ] 	
		for index, value in enumerate(intData):
			if index % 100000 == 0:
				bar.update(100*index/len(intData))
			channel = index % self.nchannels
			self.frames[channel].append(value)
		bar.finish()
			
#------------------------------------------------------------------ write wav file ------/			
	def writeWav(self, OUT_FILE, frames = None):
		if frames == None:
			frames = self.frames
		elif len(frames) != self.nchannels:
			#if frames is a list of files
			cwd = os.getcwd()
			print("cwd: {}".format(cwd))                # create new directory for chopped files
			if not os.path.exists(cwd + "/" + OUT_FILE):
				os.makedirs(cwd + "/" + OUT_FILE)

			os.chdir(cwd + "/" + OUT_FILE)
	
			for i, chop in enumerate(frames): #number the file names
				self.writeWav("{}{}.wav".format(OUT_FILE, i), chop) 
			os.chdir(cwd)
			return
		
		#if frames is a single file, not a list of files
		ww = wave.open(OUT_FILE, 'wb')
		ww.setnchannels(self.nchannels)
		ww.setsampwidth(self.sampwidth)
		ww.setframerate(self.framerate)
		ww.setnframes(self.nframes)
		ww.setcomptype(self.__comptype, self.__compname)
		
		intData = []
		
		bar = progressbar.ProgressBar()
		print("writing wave file:")
		for num in range (len(frames[0])):
			for channel in frames:
				intData.append(channel[num])
				if num % 100000 == 0:
					bar.update(100*num/len(frames[0]))
		
		bar.finish()
		print("finishing up...")
		nsamplesNew = len(intData)
		
		if self.sampwidth == 1:
			fmt = "%iB" % nsamplesNew # read unsigned chars
		elif self.sampwidth == 2:
			fmt = "%ih" % nsamplesNew # read signed 2 byte shorts
		else:
			raise ValueError("Only supports 8 and 16 bit audio formats.")
		
		intData = tuple(intData)
		newData = struct.pack(fmt, *intData)
		ww.writeframes(newData)

#------------------------------------------------------------------ add method ----------/
	def __add__(self, other):
		
		if (self.nchannels != other.nchannels or 
			self.sampwidth != other.sampwidth or
			   self.framerate != other.framerate):
			error("cannot add Wavefiles with nchannels, samplewidth or framerate")
			exit()
		
		addedFrames=copy.deepcopy(self.frames)

		for i, channel in enumerate(other.frames):
			addedFrames[i].extend(other.frames[i])
				
		temp = tempfile.NamedTemporaryFile(suffix = '.wav', delete = False) 
		self.writeWav(temp.name, addedFrames)
		newWaveFile = Wavefile(temp.name)
		#tempfile used to create new Wavefile object
		os.remove(temp.name)
		#remove temp now that we don't need it
	
		return newWaveFile
		
#--------------------------------------------------------------- documentation ----------/
	def documentation(self):
		with open("readme.txt") as file:
			text = file.read()
			return(text)



#=====================================================================[ DSP METHODS ]====/
#------------------------------------------------------------------ low pass filter -----/			
	def lowPassFilter(self, frames = None):
		if frames == None:
			frames = self.frames
	
	
		for channel in frames:
			for num in range(2, len(channel)):
				channel[num] = int((channel[num]+channel[num-1]+channel[num-2])/3)
	
		return frames
	
	#--------------------------------------------------------------- changeSpeed  -------/				
	def changeSpeed(self, speed, frames = None):
		if frames == None:
			frames = self.frames
		newFrames = []
		if speed == 0:
			error("Error: can't have speed of 0")
			return frames
		elif speed < 0:
			frames = self.reverse(frames)
			speed = abs(speed)
	
		invert = lambda x: 1/x
		speed = invert(speed)
	
		oldNumFrames = len(frames[0])
		newNumFrames = int(speed*len(frames[0]))
	
		
		print("Processing Speed Change:")
	
		for channel in frames:
			index = 0
			newChannels = []
	
			bar = progressbar.ProgressBar()

			for sample in range(newNumFrames):
				newChannels.append(channel[int(oldNumFrames/newNumFrames*sample)])
				if sample % 100000 == 0:
					bar.update(100*sample/newNumFrames)
				
			newFrames.append(newChannels)
		bar.finish()

		return newFrames
	
	#------------------------------------------------------------------- reverse --------/				
	def reverse(self, frames = None):
		if frames == None:
			frames = self.frames
		newFrames = []
	
		print("Processing Reverse:")
		bar = progressbar.ProgressBar()


		for channel in frames:
			newChannels = list(channel)
			newChannels.reverse()
			newFrames.append(newChannels)
	
		bar.update(100)
		bar.finish()

		return newFrames
	
	#------------------------------------------------------------------ granulate -------/				
	def granulate(self, grainsize, spread, speed = 1, frames = None):
		if frames == None:
			frames = self.frames
		
		if speed != 1:
			frames = self.changeSpeed(speed)
		
		newFrames = []
		oldNumFrames = len(frames[0])
	
		bar = progressbar.ProgressBar()
		print("Processing Granular Shift:")
	
	
		for channel in frames:
			newChannel = []
			for num in range(0, len(channel)-grainsize, spread):
				if num % 10000 == 0:
					bar.update(100*num/(len(channel)-grainsize))
				grain = [channel[num+i] for i in range(grainsize)]
				newChannel.extend(grain)
			newFrames.append(newChannel)
		
		bar.finish()
		
		return newFrames
	

	#---------------------------------------------------------------------- gain --------/				
	def gain(self, amt, frames = None):
		if frames == None:
			frames = self.frames
		newFrames = []
	
		print("Processing gain:")
		bar = progressbar.ProgressBar()
		bar.update(0)
		
		for i, channel in enumerate(frames):
			newChannels = list(channel)
			newChannels = list(map(lambda x: int(x*amt), newChannels))
			for j, sample in enumerate(newChannels):#clip sample values at maximum sampleDepth
				if sample > self.sampleDepth:
					newChannels[j] = self.sampleDepth
				elif sample < -self.sampleDepth:
					newChannels[j] = -self.sampleDepth
					
			newFrames.append(newChannels)
			bar.update()
	
		bar.update(100)
		bar.finish()

		return newFrames
		
		#------------------------------------------------------------------ chop --------/				
	def chop(self, chopsize, frames = None):
		if frames == None:
			frames = self.frames
		newChops = []
	
		print("Processing chop:")
		bar = progressbar.ProgressBar()
		bar.update(0)
		
		for num in range(0, len(frames[0]), chopsize):
			
		
			newFrames = []
			for channel in frames:
				newChannels = []
				newChannels.extend(channel[num:num+chopsize])
				newFrames.append(newChannels)
			newChops.append(newFrames)
			
			if num % 100 == 0:
				bar.update(100*num/len(frames[0]))
		
		bar.update(100)
		bar.finish()
	
		return newChops
			
			
			
		newFrames.append(newChannels)
	
		bar.update(100)
		bar.finish()

		return newFrames
		
#----------------------------------------------------------------------- merge ----------/				
	def merge(self, chops):
		
		newFrames = []
		
		for channels in chops[0]:
			newFrames.append([])
			
		for i, chop in (enumerate(chops)):
			for j, channel in enumerate(chop):
				newFrames[j].extend(chop[j])
				
		return newFrames
		
#======================================================================Setup=============/
print("RUNNING DSP VERSION 1.0 BETA")




