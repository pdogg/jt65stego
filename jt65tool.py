#!/usr/bin/python
#
# JT65 Steganography PoC
#
# by @pdogg77 & @TheDukeZip

import sys
import argparse
import numpy as np
import jt65wrapy as jt
import jt65stego as jts

hidekey = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]

def ValidateArguments(args):
	if args.encode and args.decode:
		print("Cannot use both --encode and --decode at the same time!")
		sys.exit(0)

	if args.interactive and args.batch:
		print("Cannot use both --interactive and --batch at the same time!")
		sys.exit(0)

# Command line argument setup
parser = argparse.ArgumentParser(description='Steganography tools for JT65 messages.', epilog="Transmitting hidden messages over amateur radio is prohibited by U.S. law.")
groupCommands = parser.add_argument_group("Commands")
groupOptions = parser.add_argument_group("Options")
groupEncryption = parser.add_argument_group("Encryption")
groupEncodeOutput = parser.add_argument_group("Encode Output")
groupDecodeInput = parser.add_argument_group("Decode Input")
groupCommands.add_argument('--encode', action='store_true', help='Encode msg(s)')
groupCommands.add_argument('--decode', action='store_true', help='Decode msg(s)')
groupOptions.add_argument('--noise', type=int, default=5, metavar='<noise>', help='Amount of cover noise to insert')
groupOptions.add_argument('--interactive', action='store_true', help='Interactive mode, prompt user for msgs (default)')
groupOptions.add_argument('--batch', action='store_true', help='Batch mode, msgs must be parameters at command line')
groupOptions.add_argument('--jt65msg', metavar='<message1(,message2)(,message3)...>', help='Message to encode in JT65 (batch mode)')
groupOptions.add_argument('--stegmsg', metavar='<message>', help='Message to hide in result (batch mode)')
groupOptions.add_argument('--verbose', action='store_true', help='Verbose output')
groupEncryption.add_argument('--cipher', default='none', metavar='<type>', help='Supported ciphers are none, XOR, ARC4, AES, GPG, OTP (default: none)')
groupEncryption.add_argument('--key', metavar='<key>', help='Cipher key (batch mode)')
groupEncryption.add_argument('--recipient', metavar='<user>', help='Recipient for GPG mode')
groupEncryption.add_argument('--aesmode', metavar='<mode>', help='Supported modes are ECB, CBC, CFB (default: ECB)')
groupEncodeOutput.add_argument('--stdout', default=True, action='store_true', help='Output to terminal (default)')
groupEncodeOutput.add_argument('--wavout', metavar='<file1.wav>', help='Output to wav file(s) - Multiple files suffix -001.wav, -002.wav...')
groupDecodeInput.add_argument('--stdin', default=True, action='store_true', help='Input from stdin (default)')
groupDecodeInput.add_argument('--wavin', metavar='<file1.wav(,file2.wav)(,file3.wav)...>', help='Input from wav file(s)')
args = parser.parse_args()

# Check arguments to make sure we have everything we need and there are no contradictory commands
ValidateArguments(args)

# Batch encode
if args.batch and args.encode:
	jts.BatchEncode(args.jt65msg, args.stegmsg, args.noise, args.cipher, args.key, args.recipient, args.aesmode, args.verbose, args.stdout, args.wavout, hidekey)

# Decode
elif args.decode:
	#Process input to JT numpy arrays
	jt65data = jts.processinput(args.stdin, args.wavin, args.verbose)

	#Retrieve JT65 valid messages
	jt65msgs = jts.decodemessages(jt65data, args.verbose)

	#Retrieve steg message
	stegdata = jts.retrievesteg(jt65data, hidekey, args.verbose)

	#Decipher steg message
	stegmsg = jts.deciphersteg(stegdata, args.cipher, args.key, args.aesmode, args.verbose)

	#Print result
	for index,value in enumerate(jt65msgs):
		print "\nDecoded JT65 message " + str(index) + " : " + value 
	print "\nHidden message : " + stegmsg
