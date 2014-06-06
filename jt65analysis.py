# basic "steganalysis" of jt65 symbol sets

import sys
import copy
import argparse
import jt65stego
import jt65wrapy
import numpy as np

def eq(a, b) :
#for map in checkpacket
  return (a == b)

def col(a, i):
    return [row[i] for row in a]
  
def checkpacket(packet) :
#packet is a two dimensional array of symbols and confidence
#returns diffs list of [diff position, packet symbol, clean encode symbol, confidence]
#if verbose prints <number of diffs>,<average confidence of diffs> to stdout
  symbols = packet[0]
  confidence = packet[1]
  
  symboltrydecode = copy.deepcopy(symbols)
  testdecode = jt65wrapy.unprepmsg(symboltrydecode)
  realmessage = jt65wrapy.prepmsg(testdecode)
  symbolmap = map(eq, realmessage, symbols)
  
  diffs = []
  conftotal = 0
  for i in range(0,63) :
    if not symbolmap[i] :
      diffs.append([ i, symbols[i], realmessage[i], confidence[i] ])
      

  
  return diffs
  
  
def output(diffs, packet) :
# formated output for a packet and some diffs
# #diffs, totalconfidence, averageconfidence, mediaconfidence, stddevconfidence, averagedistance, s2db, freq, a1, a2, decode
    conftotal = 0
    diffdist = 0
    if diffs :
      for dif in diffs:
	conftotal += dif[3]
        diffdist += abs(dif[1]-dif[2])
      print str(len(diffs)) +  ", " + str(conftotal) + ", " + str( float(conftotal) / float(len(diffs))) + ", " + str(np.median(col(diffs,3)))  + ", " + str(np.std(col(diffs,3)))+  ", " + str(diffdist/len(diffs))   +  ", " + packet[3]  +  ", " + packet[4] +  ", " + packet[5] +  ", " + packet[6] + ", " + packet[2]
    else :
      print "0, 0, 0, 0, 0, 0, " + packet[3]  +  ", " + packet[4] +  ", " + packet[5] +  ", " + packet[6] + ", " + packet[2]
if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description='Packet Steganalysis tools for JT65 messages.', epilog="Transmitting hidden messages over amateur radio is prohibited by U.S. law.")
  
  groupSource = parser.add_argument_group("Source")
  groupCommands = parser.add_argument_group("Commands")
  groupSource.add_argument('--file', metavar='<filename>', help='Read from file')
  groupCommands.add_argument('--verbose', action='store_true', help='verbosity')
  
  args = parser.parse_args()
  
  verbose = False
  #add some validation
  if args.verbose :
    verbose = True
    print args.file
  packets = jt65wrapy.decodewav(args.file)
  if verbose :
    print packets
 
  for packet in packets :
   
   diffs=checkpacket(packet)
   output(diffs,packet)
  
  
