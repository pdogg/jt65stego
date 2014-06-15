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


Build Instructions
====================

After installing dependencies "make all" in this directory should build the required library and binary from lib/

JT65.so - f2py binding library for the jt65 pack/unpack and Reed Solomon encode/decode
jt65 - Demodulation binary, reads in .wav file and outputs symbols and confidence for processing

make f2pylib
make jt65

Will build these components independently if needed


Basic Usage
===========

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
