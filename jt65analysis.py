# basic "steganalysis" of jt65 symbol sets

import sys
import copy
import argparse
import math
import csv
import jt65stego
import jt65wrapy
import numpy as np
import matplotlib.pyplot as plt

def eq(a, b) :
#for map in checkpacket
  return (a == b)

def col(a, i):
    return [float(row[i]) for row in a]

def selecterrors(errors, a):
  rows = [] 
  for row in a :
    if int(row[0]) == errors :
      rows.append(row)
  return rows

def gridtolatlon(grid) :
#takes in a maidenhead grid and returns lat, lon
#https://en.wikipedia.org/wiki/Maidenhead_Locator_System

  lon = (ord(grid[0]) - ord('A')) * 20 - 180
  lat = (ord(grid[1]) - ord('A')) * 10 - 90
  lon += (ord(grid[2]) - ord('0')) * 2
  lat += (ord(grid[3]) - ord('0')) * 1
  
# move to center of square
  lon += 1
  lat += 0.5
  
  return [lat, lon]
  
  
def distance_on_unit_sphere(lat1, long1, lat2, long2, unit=3960):
#http://www.johndcook.com/python_longitude_latitude.html
#The following code returns the distance between to locations based on each point's longitude and latitude. 
#The distance returned is relative to Earth's radius. To get the distance in miles, multiply by 3960. 
#To get the distance in kilometers, multiply by 6373.
# We default to miles...

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
	
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
	
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
	
    # Compute spherical distance from spherical coordinates.
	
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    return arc * unit
  

def getgrid(string) :
#takes in a string. If the last 4 character make up valid grid it returns them
# if they aren't a valid grid returns False
  validletters=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R"]
  
  splits = string.split()
  length = len(splits)
  
  last = splits[length-1]
  if len(last) != 4 :  # if it isn't 4 chars long it isn't a grid
    return False 
  elif last[0] not in validletters or last[1] not in validletters :
    return False  #doesn't start with two valid capital letters
  else :
    try :
      number = int(last[2:4])
      return last #it looks like a grid more or less at this point
    except :
      return False #can't convert to int
      
    

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
  
  print diffs
  print realmessage
  print symbols

  return diffs
  
  
def output(diffs, packet, distances=False, distancegrid="") :
# formated output for a packet and some diffs
# #diffs, totalconfidence, averageconfidence, mediaconfidence, stddevconfidence, averagedistance, s2db, freq, a1, a2, decode
    if distances and not getgrid(distancegrid) :
      print "you asked for distances and gave a bad or no grid... ERROR"
      return False
    elif distances :
      homelatlon = gridtolatlon(distancegrid)

#SNR logic from jt65a.f90

    snr = 10.0* math.log10(float(packet[3])) - 32
    if snr > -1 :
      snr = -1
    elif snr < -30 :
      snr = -30
      
    conftotal = 0
    diffdist = 0
    grid = getgrid(packet[2])
    distance = 0
    if distances and grid:
      gridlatlon = gridtolatlon(grid)
      distance = distance_on_unit_sphere(gridlatlon[0], gridlatlon[1], homelatlon[0], homelatlon[1])
      
    if diffs :
      for dif in diffs:
	conftotal += dif[3]
        diffdist += abs(dif[1]-dif[2])
      print str(len(diffs)) +  ", " + str(conftotal) + ", " + str( float(conftotal) / float(len(diffs))) + ", " + str(np.median(col(diffs,3)))  + ", " + str(np.std(col(diffs,3)))+  ", " + str(diffdist/len(diffs))   +  ", " + packet[3]  +  ", " + packet[4] +  ", " + packet[5] +  ", " + packet[6] + ", " + str(distance) + ", " + str(snr)  + ", " + packet[2] 
    else :
      print "0, 0, 0, 0, 0, 0, " + packet[3]  +  ", " + packet[4] +  ", " + packet[5] +  ", " + packet[6] + ", " + str(distance) + ", " + str(snr)  + ", " + packet[2]   

      
def processtextfile(filename, threshold=10) :
# process a textfile of output above and generate distance / snr / error stats
  rows = []
  f = open(filename)
  for row in csv.reader(f) :
    rows.append(row)
  errorcol = col(rows,0)
  snrcol = col(rows,11)

  print "Number of packets in file:			" + str(len(rows))
  print "\n"
  print "Median Number of Errors:			" + str(np.median(errorcol)) 
  print "Average Number of Errors:			" + str(np.average(errorcol))
  print "Standard Deviation of Errors:			" + str(np.std(errorcol))
  print "Error Bins:					\n" + str(np.bincount(errorcol, None, 63))
  print "\n"
  print "Median SNR:					" + str(np.median(snrcol)) 
  print "Average SNR:					" + str(np.average(snrcol))
  print "Standard Deviation SNR:				" + str(np.std(snrcol))
  
  errorplot = plt.figure()
  errorplot.suptitle('Error Histogram', fontsize=14, fontweight='bold')
  axerror = errorplot.add_subplot(111)
  numbins = max(errorcol)
  axerror.hist(errorcol,numbins,color='red',alpha=0.8)
  errorplot.show()
  
  inrangepackets = []
  for i in range(0, threshold + 1):
    setpackets = selecterrors(i, rows)
    inrangepackets +=  setpackets
    
  print "\n"
  print "Number of packets in set with " + str(threshold) +" or less errors: " + str(len(inrangepackets))
  
  distances = []
  for entry in col(inrangepackets,10) :
      if entry != 0 :
       distances.append(entry)
  print "	" + str(len(distances)) + " have distance data"
  print "	Max Distance of Set:			" + str(np.amax(distances))
  print "	Median Distance of Set:			" + str(np.median(distances)) 
  print "	Average Distance of Set:		" + str(np.average(distances))
  print "	90% Distance of Set:			" + str(np.percentile(distances,90))

  distplot = plt.figure()
  distplot.suptitle('Distances for errors <= ' + str(threshold), fontsize=14, fontweight='bold')
  axdist = distplot.add_subplot(111)
  numbins = 10
  axdist.hist(distances,numbins,color='green',alpha=0.8)
  distplot.show()
   
  heatplot = plt.figure()
  heatplot.suptitle('Errors / std(confidence) ', fontsize=14, fontweight='bold')
  axheat = heatplot.add_subplot(111)
  axheat.hexbin(errorcol,col(rows,4), bins='log', gridsize=200, cmap=plt.cm.bone)
  heatplot.show()
  
  heatplot2 = plt.figure()
  heatplot2.suptitle('Errors / avg(confidence) ', fontsize=14, fontweight='bold')
  axheat2 = heatplot2.add_subplot(111)
  axheat2.hexbin(errorcol,col(rows,2), bins='log', gridsize=200, cmap=plt.cm.bone)
  heatplot2.show()
  
  heatplot3 = plt.figure()
  heatplot3.suptitle('Errors / snr ', fontsize=14, fontweight='bold')
  axheat3 = heatplot3.add_subplot(111)
  axheat3.hexbin(errorcol,snrcol, bins='log', gridsize=200, cmap=plt.cm.bone)
  heatplot3.show()
  
  

      
if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description='Packet Analysis tools for JT65 messages.', epilog="Transmitting hidden messages over amateur radio is prohibited by U.S. law.")
  
  groupSource = parser.add_argument_group("Source")
  groupCommands = parser.add_argument_group("Commands")
  groupOptions = parser.add_argument_group("Options")
  groupOptions.add_argument('--distance', metavar='<gridloc>', help='calc distance from grid')
  groupSource.add_argument('--file', metavar='<filename>', help='Read from and parse wav file')
  groupSource.add_argument('--text', metavar='<textfile>', help='Read from and parse a text file for distance and snr stats')
  groupCommands.add_argument('--verbose', action='store_true', help='verbosity')
  
  args = parser.parse_args()
  
  verbose = False
  #add some validation
  if args.verbose :
    verbose = True
    print args.file

#decode a wav file    
  if args.file : 
    sys.stderr.write("processing: " + args.file + "\n")
    packets = jt65wrapy.decodewav(args.file)
    if verbose :  
      print packets
    homegrid = ""
    dodistance = False
    if args.distance :
      homegrid = args.distance
      dodistance = True 
    for packet in packets :  
     diffs=checkpacket(packet)
     output(diffs,packet, dodistance, homegrid)
  
  
#decode a text file

  if args.text :
    processtextfile(args.text)
    raw_input("Press Enter to continue...")