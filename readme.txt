README.txt for 'wav.py' and 'dsp.py'
by Isaac Sleator [ics2106]
COMS W3101: Programming Languages (Python) 
FINAL PROJECT

-----------------------------------------------------------------------------------------
Included Files:
	wav.py - main method
	dsp.py - dsp module
	jdilla.wav - testfile
	martin.wav - testfile
	readme.txt - manual

-----------------------------------------------------------------------------------------
About:
	This program makes use of the wave module to read .wav files, and manipulate the data
	contained inside. Each .wav file is instantiated as a Wavefile class, which contains
	a number of audio processing algorithms that can be applied to the data and written
	back into a .wav file.
	
	wav.py contains the main method and testing methods
	dsp.py contains the Wavefile class and DSP functions, and a little ex. script

-----------------------------------------------------------------------------------------
Requirements:
	•System requires python3
	•wav.py requires mplayer [brew install mplayer]
	•required modules: (wave, re, os, random, sys, time, struct, progressbar, math,
	 logging, copy and tempfile)

-----------------------------------------------------------------------------------------
Wavefile Class Documentation[in dsp.py]:
	PUBLIC VARIABLES
	• self.filename = the name of initializing file
	• self.nchannels = the number of audio channels in Wavefile
	• self.sampwidth = the bit depth (1 = 8bit, 2 = 16bit, etc)
	• self.framerate = the sample rate (samples per second)
	• self.nframes = the total number of frames per channel
	• self.nsamples = the total number of frames in all channels
	• self.frames = sample data in usable, integer list form: [[ch1][ch2]] where each inner
					list is a list of samples for each channel (^^ in this case 2)
	• self.name = name of file without .wav
						
	DEFINED FUNCTIONS
	• __init__(IN_FILE) 
		takes a .wav file from disk and instantiates a new object
		
	• __add__(self, other)
		takes two Wavefile objects and concatenates their audio data starting with
		self, ending with other
	
	• documentation(self)
		returns this readme.txt file
		
	• writeWav(self, OUT_FILE, frames = None)
		writes a .wav, or group of wav files to disk. If a list of custom frames is not
		specified, the function will use the frames from the original file. Function can
		also take a list of frame lists, (like the output of chop) and write each one
		as its own file
		
	• lowPassFilter(self, frames = None)
		uses a basic averaging algorithm to create a subtle lowpass filter. Returns
		frames list with values that have been low-pass-filtered
		
	• changeSpeed(self, speed, frames = None)
		changes the speed of file by removing or duplicating frames. Returns new list
		of frames
		
	• reverse(self, frames = None)
		returns reversed list of frames
		
	• granulate(self, grainsize, spread, speed = 1, frames = None)
		A granulator synth algorithm that plays through file data in chunks, called
		grains, whose size is specified by grainsize, and the separation of each grain
		is specified by spread. Optional speed algorithm built in.
	
	• gain(self, amt, frames = None)
		An easy signal gain control. Clips values that exceed the minimum/maximum
		possible sample values
		
	• chop(self, chopsize, frames = None)
		chops audio data into slices, and returns all slices as a big list of slices
		
	• merge(self, chops)
		takes a list of slices (chops) and merges them into one, concatenated
		list of frames.	
-----------------------------------------------------------------------------------------
Testing:
	•please make sure all modules and external programs have been installed
	
	•to test with my included examples in a directory of your choice,
	enter in command line: 
	
		'python3 wav.py martin.wav jdilla.wav tests/'
	
	where 'tests/' is the directory you wish to store your test files. If the 4th
	command line argument is not given, the program will output test .wav files to 
	the current working directory instead. Chopped folders are stored to cwd/[chopname], 
	regardless of 4th command line arg. 
	
	•program will run through a series of examples, using the functions listed above,
	outputting a number of different files, which will then be opened and played in
	the shell using mplayer. Each outputted file will play in order and program will
	exit smoothly after all files have been played.
	
	•if for any reason you need to exit the program while listening to the examples,
	hit ctrl-C multiple times, and you should be able to exit.
		
	•IF you would like to use your own 8 or 16 bit pcm wav files, feel free to
	replace martin.wav and jdilla.wav with your own files. Keep in mind that 
	long .wav files will take a significant amount of time to process, and
	it is best to use short files for testing

-----------------------------------------------------------------------------------------
Mandatory Features:
	•global variable - wav.py has a global directory variable for output files
	•Local Variables - all over the code
	•Len - used throughout
	•map - in Wavefile.gain() function, maps scaled samples
	•in - used throughout
	•list comprehension - used in Wavefile __init__ function to set up frame lists
	•list - used throughout
	•str - used throughout
	•range - used throughout
	•if, with at least one else/elif - used throughout
	•for loop - used throughout
	•while loop - used in wav.py while sequencing output files
	•try and except - wav.py specifies assertion error during testing
	•Any custom function - found throughout Wavefile class
	•A function with optional arguments - The Wavefile functions have optional argument for a list of frames
	•A recursive function - writeWav function is recursive if given a list of slices
	•A function defined using lambda - changeSpeed function 'invert' is defined using lambda
	-A function that changes 1 argument - 
	•A function that changes a global variable - in wav.py, getArgs parses args and changes global variable
	-A function that outputs a function - 
	•Any custom class - Wavefile class in wav.py
	-A subclass
	-An iterable class
	•A private field or method - self.__data, self.__comptype, self.__compname in Wavefile
	•A public field or method - self.frame, all functions in Wavefile class
	•A class that supports an arithmetic operation - Wavefile class supports __add__
	-A class that supports reading or writing an indexed or keyed element
	•A custom module, in addition to the main script - dsp.py
	•A mandatory command line option - two .wav files must be specified as argv[1] and argv[2]
	•An optional command line option - optional argv[3] is directory for output files
	•Reading from file - wave.open reads .wav files
	•Writing to file - wave.writeframes writes to .wav files. I Also used tempfile in __add__ function
	•5 distinct test cases - I have 13 test cases
	•Any assertion - used assertion to assert that __add__ function works correctly
	
Optional Features:
	•dict - used in wav.py to store playlist
	•tuple - use tuple in writeWav function of Wavefile class
	•slicing a list - chop function in Wavefile class slices Frames list [foo:foo]
	•A custom module that can also be used as script - Run dsp.py as script, it outputs the version number
	•A with block - documentation function in Wavefile uses With block
	•Logging - logging used in dsp.py class, in __.add__ and changeSpeed() functions
	•Running another (Linux) program - calls to mplayer to play outputted test files
	•Regular expression searching - in Wavefile __init__ function
-----------------------------------------------------------------------------------------
