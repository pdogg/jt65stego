import numpy as np
import pygame
from pygame.locals import *
import math

##some functions to calculate the tone values in hz for jt65 messages
## key function to call is tonewithsync it does all the work
## play these at  0.372 s each and you're done :)


def tone(number, m=1, offset=0):
##return a tone in HZ for the input number specified
#"Each channel symbol generates a tone at frequency 1270.5 + 2.6917 (N+2) m Hz, where N is
#the integral symbol value, 0 <=N >= 63, and m assumes the values 1, 2, and 4 for JT65 sub-
#modes A, B, and C."

	return offset + 1270.5 + (2.6917 * (number + 2 ) * m)

def tonepacket(message, m=1, offset=0):
#takes in a message array and returns an array of tones representing the jt65 audio tones in the message

	output = np.array(range(63),dtype=np.float)
	for x in range(0,63):
		output[x] = tone(message[x], m, offset)
	return output

def toneswithsync(message, m=1, offset=0):
## take in a jt65 packet and return a full set of tone values, ready to go with sync vector already calcualted in
# this is HZ ready to covert to audio and put out on the wire
#m is 1 2 or 4 for submodes a b and c
#offset is frequency offset
	output = np.array(range(125),dtype=np.float)
	synctone = 1270.5 + offset
	messagetones = tonepacket(message, m, offset)
	messageindex = 0
#the mystic 'pseudo-random sequence"
	syncvector = [1,0,0,1,1,0,0,0,1,1,1,1,1,1,0,1,0,1,0,0,0,1,0,1,1,0,0,1,0,0,0,1,1,1,0,0,1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,1,1,0,1,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1]
	for x in range(0,125):
		if syncvector[x] == 1:
			output[x] = synctone
		else:
			output[x] = messagetones[messageindex]
			messageindex += 1
	
	return output

def outputpygame(tones):
    
  size = (1366, 720)

  bits = 16

  pygame.mixer.pre_init(44100, -bits, 2)
  pygame.init()
  _display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)


  duration = 1        # in seconds

  for index in range(0,125):
    #freqency for the left speaker
    frequency_l = tones[index]
    #frequency for the right speaker
    frequency_r = tones[index]

    #this sounds totally different coming out of a laptop versus coming out of headphones

    sample_rate = 44100

    n_samples = int(round(duration*sample_rate))
    #n_samples = 4096
	#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = np.zeros((n_samples, 2), dtype = np.int16)
    max_sample = 2**(bits - 1) - 1

    for s in range(n_samples):
	  t = float(s)/sample_rate    # time in seconds

	  #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
	  buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
	  buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right

    sound = pygame.sndarray.make_sound(buf)
#play once, then loop forever
    sound.play()



  pygame.quit()
 
  
  