# basic "steganalysis" of jt65 symbol sets
# example data:
#13 43 15 35 30 5 46 10 61 55 26 26 41 55 17 61 25 62 5 15 52 56 40 28 5 33 4 43 0 3 42 32 25 31 48 38 23 23 13 5 52 62 57 48 47 11 21 1 61 4 15 50 41 49 26 28 62 59 4 33 53 53 60
#255 255 255 255 255 227 255 254 255 255 255 255 255 255 255 255 255 255 228 255 255 255 255 255 227 255 216 255 221 213 255 255 255 255 255 255 255 255 255 221 255 255 255 255 255 255 255 190 255 222 255 255 255 255 255 255 255 255 220 255 255 255 255
#
# Where first line is symbols and second line is confidence (prob in wsjtx etc)
# probability optional
import sys
import copy
import argparse
import jt65stego
import jt65wrapy

def readfile(filename) :
# read in a file and return a list containing the values of each line as a list
# only supports one line in the file!!! FIX FIX!!

  rows = []
  f = open(filename)
  lines = f.readlines()
  for line in lines :
      row = [int(n) for n in line.split()]
      rows.append(row)
  
  return rows

def eq(a, b) :
#for map in checkpacket
  return (a == b)
  
  
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
      conftotal += confidence[i]
  if diffs and verbose:    
    print str(len(diffs)) +  "," + str(conftotal / len(diffs))
  
  return diffs
  
  


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
  packets = readfile(args.file)
  if verbose :
    print packets
    
  checkpacket(packets)
  
  
