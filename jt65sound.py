import numpy as np

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

