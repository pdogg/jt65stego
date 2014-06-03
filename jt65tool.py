#!/usr/bin/python
#
# JT65 Steganography PoC
#
# by @pdogg77 & @TheDukeZip

import sys
import argparse
import copy
import time
import datetime
import subprocess
import os
import time
import thread
import colorama
import numpy as np
import jt65stego as jts
import jt65sound

STEG_ENABLED = True
STEG_DETECTION_ERROR_THRESHOLD = 17
hidekey = []

def ValidateArguments(args):
	if args.encode and args.decode:
		print("Cannot use both --encode and --decode at the same time!")
		sys.exit(0)

	if args.interactive and args.batch:
		print("Cannot use both --interactive and --batch at the same time!")
		sys.exit(0)

def SetArgumentDefaults(args):
	if not args.stdout and not args.wavout:
		args.stdout = True

	if not args.stdin and not args.wavin:
		args.stdin = True

def processoutput(finalmsgs, stdout, wavout, wsjt, verbose):
#Send JT65 messages to output specified by user
	if stdout:
		np.set_printoptions(linewidth=300)

		for msg in finalmsgs:
			print msg

	if wavout:
		wavmode = 1 	#Set mode to WSJT-X

		if wsjt:
			wavmode = 0

		if wavout.endswith('.wav'):
			wavout = wavout[:-4]

		for index,value in enumerate(finalmsgs):
			filename = wavout + "-" + str(index).zfill(3) + ".wav"

			if verbose:
				print "Generating audio file " + str(index) + " : " + filename
				
			tones = jt65sound.toneswithsync(value)
			jt65sound.outputwavfile(filename, tones, wavmode)

def processinput(stdin, wavin, verbose):
#Process input from stdin or wavs and return array of JT65 data
	JT65data = []

	if stdin:
		stdinput = sys.stdin.readlines()

		n = 0 

		for index,value in enumerate(stdinput):
			if value.startswith("["):				#Filter to only JT65 messages, allows usage with output from --encode --verbose
				if verbose:
					print "Raw Message " + str(n) + " : " + value

				numpymsg = np.fromstring(value.replace('[','').replace(']',''), dtype=int, sep=' ')
				JT65data.append(numpymsg)
				n = n + 1

			elif verbose:
				print value  #Shows any warnings, errors, or verbose output from stdin

	elif wavin:
		wavfiles = wavin.split(",")

		for index,value in enumerate(wavfiles):
			messages = jt65sound.inputwavfile(value, verbose)

			for currentmsg in messages:
				symbols, confidence, msg, s2db, freq, a1, a2 = currentmsg
				numpymsg = np.array(symbols)
				JT65data.append(numpymsg)

	return JT65data

def performwavdecode(filename):
	containssteg = False
	messages = jt65sound.inputwavfile(filename, verbose=args.verbose)

	for currentmsg in messages:
		symbols, confidence, msg, s2db, freq, a1, a2 = currentmsg
		numpymsg = np.array(symbols)
		jt65data = []
		jt65data.append(numpymsg)
		jt65datacopy = copy.deepcopy(jt65data)	#Necessary on some version of Python due to 'unprepmsg' not preserving list

		#Retrieve JT65 valid messages
		jt65msgs = jts.decodemessages(jt65data, args.verbose)

		if STEG_ENABLED:
			containssteg = jts.validatesteg(jt65msgs[0], symbols, hidekey, STEG_DETECTION_ERROR_THRESHOLD, args.verbose)

		if containssteg:
			#Retrieve steg message
			stegdata = jts.retrievesteg(jt65datacopy, hidekey, args.verbose)

			#Decipher steg message
			stegmsg = jts.deciphersteg(stegdata, args.cipher, args.key, args.aesmode, args.verbose)

		#Print result
		for index,value in enumerate(jt65msgs):
			print "\nDecoded JT65 message " + str(index) + " : " + colorama.Fore.BLUE + value + colorama.Fore.RESET

		if containssteg:
			print "\nHidden message : " + colorama.Fore.RED + stegmsg + colorama.Fore.RESET

# Command line argument setup
parser = argparse.ArgumentParser(description='Steganography tools for JT65 messages.', epilog="Transmitting hidden messages over amateur radio is prohibited by U.S. law.")
groupCommands = parser.add_argument_group("Commands")
groupOptions = parser.add_argument_group("Options")
groupEncryption = parser.add_argument_group("Encryption")
groupEncodeOutput = parser.add_argument_group("Encode Output")
groupDecodeInput = parser.add_argument_group("Decode Input")
groupCommands.add_argument('--encode', action='store_true', help='Encode msg(s)')
groupCommands.add_argument('--decode', action='store_true', help='Decode msg(s)')
groupOptions.add_argument('--noise', type=int, default=0, metavar='<noise>', help='Amount of cover noise to insert (default: 0)')
groupOptions.add_argument('--interactive', action='store_true', help='Interactive mode, prompt user for msgs (default)')
groupOptions.add_argument('--batch', action='store_true', help='Batch mode, msgs must be parameters at command line')
groupOptions.add_argument('--jt65msg', metavar='<message1(,message2)(,message3)...>', help='Message to encode in JT65 (batch mode)')
groupOptions.add_argument('--stegmsg', metavar='<message>', help='Message to hide in result (batch mode)')
groupOptions.add_argument('--verbose', action='store_true', help='Verbose output')
groupEncryption.add_argument('--cipher', default='none', metavar='<type>', choices=['none', 'XOR', 'ARC4', 'AES', 'GPG', 'OTP'], help='Supported ciphers are none, XOR, ARC4, AES, GPG, OTP (default: none)')
groupEncryption.add_argument('--key', metavar='<key>', help='Cipher/steg symbol key (batch mode)')
groupEncryption.add_argument('--recipient', metavar='<user>', help='Recipient for GPG mode')
groupEncryption.add_argument('--aesmode', default='ECB', metavar='<mode>', choices=['ECB', 'CBC', 'CFB'], help='Supported modes are ECB, CBC, CFB (default: ECB)')
groupEncodeOutput.add_argument('--stdout', action='store_true', help='Output to terminal (default)')
groupEncodeOutput.add_argument('--wavout', metavar='<file1.wav>', help='Output to wav file(s) - Multiple files suffix -001.wav, -002.wav...')
groupEncodeOutput.add_argument('--wsjt', action='store_true', help='Output wav file compatible with WSJT instead of WSJT-X')
groupDecodeInput.add_argument('--stdin', action='store_true', help='Input from stdin (default)')
groupDecodeInput.add_argument('--wavin', metavar='<file1.wav(,file2.wav)(,file3.wav)...>', help='Input from wav file(s)')
args = parser.parse_args()

colorama.init()

# Check arguments to make sure we have everything we need and there are no contradictory commands
ValidateArguments(args)
SetArgumentDefaults(args)

if not args.key:
	print colorama.Fore.RED + "No steg symbol key provided, steganography mode disabled" + colorama.Fore.RESET
	STEG_ENABLED = False
else:
	hidekey = jts.getnoisekey(args.key)

# Batch encode
if args.batch and args.encode:
	#Create array of your valid JT65 text
	jt65msgs = args.jt65msg.split(',')

	#Create array of valid JT65 data
	jt65data = jts.jt65encodemessages(jt65msgs, args.verbose)

	if args.stegmsg != "" and STEG_ENABLED:
		#Create array of cipher data to hide
		cipherdata = jts.createciphermsgs(len(jt65data), args.stegmsg, args.cipher, args.key, args.recipient, args.aesmode, args.verbose)

		#Embed steg data in JT65 messages
		finalmsgs = jts.steginject(jt65data, args.noise, cipherdata, hidekey, args.verbose)

	else:
		#No steg data to hide, just add cover noise if specified
		finalmsgs = []
		for msg in jt65data:
			finalmsgs.append(jts.randomcover(msg,[],args.noise,args.verbose))

	#Send to output
	processoutput(finalmsgs, args.stdout, args.wavout, args.wsjt, args.verbose)

# Decode
elif args.decode:
	stegpresent = False

	#Process input to JT numpy arrays
	jt65data = processinput(args.stdin, args.wavin, args.verbose)
	jt65datacopy = copy.deepcopy(jt65data)
	jt65stegmsgs = []

	#Retrieve JT65 valid messages
	jt65msgs = jts.decodemessages(jt65data, args.verbose)

	if STEG_ENABLED:
		for i in range(len(jt65datacopy)):
			if jts.validatesteg(jt65msgs[i], jt65datacopy[i], hidekey, STEG_DETECTION_ERROR_THRESHOLD, args.verbose):
				jt65stegmsgs.append(jt65datacopy[i])
				stegpresent = True

	#Retrieve steg message
	stegdata = jts.retrievesteg(jt65stegmsgs, hidekey, args.verbose)

	#Decipher steg message
	stegmsg = jts.deciphersteg(stegdata, args.cipher, args.key, args.aesmode, args.verbose)

	#Print result
	for index,value in enumerate(jt65msgs):
		print "\nDecoded JT65 message " + str(index) + " : " + colorama.Fore.BLUE + value + colorama.Fore.RESET
	if stegpresent:
		print "\nHidden message : " + colorama.Fore.RED + stegmsg + colorama.Fore.RESET

# Interactive - Just listening for now
elif args.interactive:

	while True:
		#Wait for start of minute
		print "Waiting for start of minute..."
		while datetime.datetime.now().second != 0:
			time.sleep(0.1)

		filename = time.strftime("logs/%Y%m%d-%H%M.wav")

		print "Monitoring..."
		with open(os.devnull, "w") as fnull:
			subprocess.call(["./jt65recorder.py", filename], stdout=fnull, stderr=fnull)

		print "Decoding..."
		thread.start_new_thread(performwavdecode, (filename,))	#Start in new thread so slower machines won't miss next msg
