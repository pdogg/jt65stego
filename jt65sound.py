#!/usr/bin/env python
#
# some functions to calculate the tone values in hz for jt65 messages
# key function to call is tonewithsync it does all the work
# play these at  0.372 s each and you're done :)
#
# Copyright 2014 - Paul Drapeau and Brent Dukes
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import numpy as np
import math
import wave
import sys
import struct
import jt65wrapy as jt
import jt65soundlookup as jtl


def tone(number, m=1, offset=0):
# return a tone in HZ for the input number specified
#"Each channel symbol generates a tone at frequency 1270.5 + 2.6917 (N+2) m Hz, where N is
# the integral symbol value, 0 <=N <= 63, and m assumes the values 1, 2, and 4 for JT65 sub-
# modes A, B, and C."

    return offset + 1270.5 + (2.6917 * (number + 2) * m)


def tonepacket(message, m=1, offset=0):
# takes in a message array and returns an array of tones representing the
# jt65 audio tones in the message

    output = np.array(range(63), dtype=np.float)
    for x in range(0, 63):
        output[x] = tone(message[x], m, offset)
    return output


def toneswithsync(message, m=1, offset=0):
# take in a jt65 packet and return a full set of tone values, ready to go with sync vector already calcualted in
# this is HZ ready to covert to audio and put out on the wire
# m is 1 2 or 4 for submodes a b and c
# offset is frequency offset
    output = np.array(range(126), dtype=np.float)
    synctone = 1270.5 + offset
    messagetones = tonepacket(message, m, offset)
    messageindex = 0
# the mystic 'pseudo-random sequence"
    syncvector = [
        1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0,
        0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    for x in range(0, 126):
        if syncvector[x] == 1:
            output[x] = synctone
        else:
            output[x] = messagetones[messageindex]
            messageindex += 1

    return output


def outputwavfile(filename, tones, mode=1):
 # Creates .wav file with tones for broadcast
 # or for decoding in JT-65 tools
 #
 # Mode 0: Decodable by WSJT
 # Mode 1: Decodable by WSJT-X

    if mode == 0:
        # WSJT
        data_size = 4096  # samples per jt65 symbol
        frate = 11025.0  # framerate as a float

    elif mode == 1:
        # WSJT-X
        data_size = 4464  # samples per jt65 symbol
        frate = 12000.0  # framerate as a float

    else:
        print("Unsupported wav file output mode : " + mode)
        sys.exit(0)

    wav_file = wave.open(filename, "w")

    amp = 1000.0     # multiplier for amplitude
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = frate * 60  # one full minute of audio
    comptype = "NONE"
    compname = "not compressed"

    values = []
    packed_zeros = struct.pack('h', int(0))

    wav_file.setparams(
        (nchannels, sampwidth, framerate, nframes, comptype, compname))

    # Enjoy 1 second of silence (jt65 specs say start tx 1 sec after start of
    # min)
    for i in range(0, framerate):
        values.append(packed_zeros)

    # Generate the 126 tones for the wav file
    for index in range(0, 126):
        sine_list_x = []
        for x in range(data_size):
            sine_list_x.append(
                math.sin(2 * math.pi * tones[index] * (x / frate)))
        for s in sine_list_x:
            packed_value = struct.pack('h', int(s * amp / 2))
            values.append(packed_value)

    # Finish out the minute with silence for the decoders to be happy with the
    # .wav file
    for i in range(0, (framerate * 59) - (126 * data_size)):
        values.append(packed_zeros)

    # Write to file
    value_str = ''.join(values)
    wav_file.writeframes(value_str)
    wav_file.close()

    return filename


def outputwavfilequick(filename, tones):
 # Creates .wav file with tones for broadcast
 # or for decoding in JT-65 tools
 # Uses a lookup table to generate the wav file very fast
 #
 # Only creates wav file quickly under the following conditions:
 #   WSJTX mode (no WSJT compatibility)
 #   JT65A
 #   Sync tone at 1270.5 Hz

    data_size = 4464  # samples per jt65 symbol
    frate = 12000.0  # framerate as a float

    wav_file = wave.open(filename, "w")

    amp = 1000.0     # multiplier for amplitude
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = frate * 60  # one full minute of audio
    comptype = "NONE"
    compname = "not compressed"

    values = []
    packed_zeros = struct.pack('h', int(0))

    wav_file.setparams(
        (nchannels, sampwidth, framerate, nframes, comptype, compname))

    # Create a list of the 126 symbols for audio with 'S' representing the sync tone
    output = [0] * 126
    messageindex = 0
    # the mystic 'pseudo-random sequence"
    syncvector = [
        1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0,
        0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    for x in range(0, 126):
        if syncvector[x] == 1:
            output[x] = 'S'
        else:
            output[x] = tones[messageindex]
            messageindex += 1

    # Enjoy 1 second of silence (jt65 specs say start tx 1 sec after start of
    # min)
    for i in range(0, framerate):
        values.append(packed_zeros)

    # Generate the 126 tones for the wav file
    for index in range(0, 126):
        if output[index] == 'S':
            for s in jtl.toneSync:
                packed_value = struct.pack('h', s)
                values.append(packed_value)
        else:
            for s in jtl.toneTable[output[index]]:
                packed_value = struct.pack('h', s)
                values.append(packed_value)

    # Finish out the minute with silence for the decoders to be happy with the
    # .wav file
    for i in range(0, (framerate * 59) - (126 * data_size)):
        values.append(packed_zeros)

    # Write to file
    value_str = ''.join(values)
    wav_file.writeframes(value_str)
    wav_file.close()

    return filename


def inputwavfile(filename, verbose=False):
# Performs decoding of JT65 wav file

    messages = jt.decodewav(filename)

    if verbose:
        for currentmsg in messages:
            symbols, confidence, jt65msg, s2db, freq, a1, a2 = currentmsg

            print "Decoded file : " + filename
            print "Symbols : " + str(symbols)
            print "Confidence : " + str(confidence)
            print "JT65 Msg : " + jt65msg
            print "S2DB : " + s2db
            print "Freq : " + freq
            print "a1 : " + a1
            print "a2 : " + a2

    return messages
