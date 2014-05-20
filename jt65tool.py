#!/usr/bin/python
#
# JT65 Steganography PoC
#
# by @pdogg77 & @TheDukeZip

import argparse

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
groupEncryption.add_argument('--cipher', metavar='<type>', help='Supported ciphers are none, XOR, ARC4, AES, GPG, OTP (default: none)')
groupEncryption.add_argument('--key', metavar='<key>', help='Cipher key (batch mode)')
groupEncryption.add_argument('--recipient', metavar='<user>', help='Recipient for GPG mode')
groupEncryption.add_argument('--aesmode', metavar='<mode>', help='Supported modes are ECB, CBC, CFB (default: ECB)')
groupEncodeOutput.add_argument('--stdout', action='store_true', help='Output to terminal (default)')
groupEncodeOutput.add_argument('--wavout', metavar='<file1.wav>', help='Output to wav file(s) - Multiple files suffix -001.wav, -002.wav...')
groupDecodeInput.add_argument('--stdin', action='store_true', help='Input from stdin (default)')
groupDecodeInput.add_argument('--wavin', metavar='<file1.wav(,file2.wav)(,file3.wav)...>', help='Input from wav file(s)')

args = parser.parse_args()
