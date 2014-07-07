jt65stego
=========

This tool has been developed by pdogg and thedukezip for the purposes of theoretical study and education on the topic
of steganography in the JT65 amateur radio protocol. 


47 CFR §97 - Rules of the Amateur Radio Service

Subpart A—General Provisions

§97.113 Prohibited transmissions.

(a) No amateur station shall transmit:
(4) Music using a phone emission except as specifically provided elsewhere in this section; communications intended to facilitate a criminal act; messages encoded for the purpose of obscuring their meaning, except as otherwise provided herein; obscene or indecent words or language; or false or deceptive messages, signals or identification.

Dependencies
============
You'll need a fortran and c compiler (most of our testing was done with gcc version 4.7.2 on Debian Wheezy, although
we have made this work on Raspian, Ubuntu 14.04, Ubuntu 13.10)

Debian Wheezy Required Additional Packages:
```
gfortran
libfftw3-dev
python-dev
python-crypto
python-gnupg
python-colorama
python-matplotlib
````

Build Instructions
====================

After installing dependencies "make all" in this directory should build the required library and binary from lib/

* JT65.so - f2py binding library for the jt65 pack/unpack and Reed Solomon encode/decode
* jt65 - Demodulation binary, reads in .wav file and outputs symbols and confidence for processing

To build these components independently if needed:

* make f2pylib
* make jt65



Basic Usage
===========

```
usage: jt65tool.py [-h] [--encode] [--decode] [--noise <noise>]
                   [--interactive] [--batch]
                   [--jt65msg <message1,message2)(,message3)...>]
                   [--stegmsg <message>] [--verbose] [--cipher <type>]
                   [--key <key>] [--recipient <user>] [--aesmode <mode>]
                   [--stdout] [--wavout <file1.wav>] [--wsjt] [--stdin]
                   [--wavin <file1.wav(,file2.wav)(,file3.wav...>]

Steganography tools for JT65 messages.

optional arguments:
  -h, --help            show this help message and exit

Commands:
  --encode              Encode msg(s)
  --decode              Decode msg(s)

Options:
  --noise <noise>       Amount of cover noise to insert (default: 0)
  --interactive         Interactive mode, prompt user for msgs (default)
  --batch               Batch mode, msgs must be parameters at command line
  --jt65msg <message1(,message2)(,message3)...>
                        Message to encode in JT65 (batch mode)
  --stegmsg <message>   Message to hide in result (batch mode)
  --verbose             Verbose output

Encryption:
  --cipher <type>       Supported ciphers are none, XOR, ARC4, AES, GPG, OTP
                        (default: none)
  --key <key>           Cipher/steg symbol key (batch mode)
  --recipient <user>    Recipient for GPG mode
  --aesmode <mode>      Supported modes are ECB, CBC, CFB (default: ECB)

Encode Output:
  --stdout              Output to terminal (default)
  --wavout <file1.wav>  Output to wav file(s) - Multiple files suffix
                        -001.wav, -002.wav...
  --wsjt                Output wav file compatible with WSJT instead of WSJT-X

Decode Input:
  --stdin               Input from stdin (default)
  --wavin <file1.wav(,file2.wav)(,file3.wav)...>
                        Input from wav file(s)
```

```
usage: jt65analysis.py [-h] [--distance <gridloc>] [--file <filename>]
                       [--simfile <filename>] [--dir <dirname>]
                       [--text <textfile>] [--verbose]

Packet Analysis tools for JT65 messages.

optional arguments:
  -h, --help            show this help message and exit

Source:
  --file <filename>     Read from and parse wav file
  --simfile <filename>  Read from and parse a text file containing jt65
                        decodes
  --dir <dirname>       Read from and parse all wav files in a given path
  --text <textfile>     Read from and parse a text file for distance and snr
                        stats

Commands:
  --verbose             verbosity

Options:
  --distance <gridloc>  calc distance from grid

Transmitting deceptive message over amateur radio in the US is a violation of
FCC regulations

```

Primarily this tool manipulates a packet data structure which is implemented as a python list as follows [[63 packet
symbols], [63 confidence values], decoded JT65 message, s2db from decoder, freq from decoder, a1 from decoder, a2 from
decoder, [list of diffs where a diff is [location, received symbol, expected symbol, confidence]]]

Input methods include reading a .wav file with the --file option, a text file containing a series of the three line
outputs from the ./jt65 binary with the --simfile option and a complete folder of .wav files with the --dir option.

These modes of operation also take in a --distance argument which calculates distance from the maidenhead grid location
provided where possible based on grid location information found in the packets.

The –text option can be used to read in this processed output and produce graphics based on the statistical calculations
performed. 

```
Examples:
python jt65analysis.py --distance DD42 --simfile 20mdecodes.txt
python jt65analysis.py --distance DD42 --file ./140527_0930.wav
python jt65analysis.py --distance DD42 --text outputfrompreviousstep.txt
```

Other functions are usable by importing the jt65analysis module. The most useful of which for analysis purposes are the
binpacketsbyerror and signalbins functions which will return packets and packet counts “binned” by various parameters.

The functions getgoodconfidence, spreadgoodconfidence, simulateerrors, and simulatespecific are used in crafting packet
characteristics from actual received datasets. These functions were used in various distance and error condition
simulations.

Credits, Thanks, and License Notes
==================================

Thanks to all @masshackers for listening to us and providing feedback over the course of the development of this tool
and this project.

The lib/ library is derived from the JT65/JT9 etc. library released under GPL as part of the WSJT-X source
originally authored by Joe Taylor K1JT and available from: http://www.physics.princeton.edu/pulsar/K1JT/devel.html
Many files have been modified for use in the JT65Stego project in May/June of 2014 by
Paul Drapeau and Brent Dukes and this version of the library should not be used for any purpose
other than the study of steganography in these protocols. It should not be considered a reliable replacement
for the libraries distributed with WSJT-X.

The RS encoder and decoder distributed with WSJT-X is Copyright 2002, Phil Karn KA9Q and labeled "May be used under the terms of the 
GNU General Public License (GPL)" These files have also been modifed by Paul Drapeau and Brent Dukes (2014) and these versions
should not be used for any purpose other than the study of steganography in these protocols. These files should not be considered
a reliable replacement for the libraries distributed with WSJT-X.
