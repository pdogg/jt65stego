subroutine timer(dname,k)
! made this a do nothing function to get temp performance improvement in ./jt65

!This library is derived from the JT65/JT9 etc. library released under GPL as part of the WSJT-X source
!originally authored by Joe Taylor K1JT and available from: http://www.physics.princeton.edu/pulsar/K1JT/devel.html!
!Many files have been modified for use in the JT65Stego project in May/June of 2014 by
!Paul Drapeau and Brent Dukes and this version of the library should not be used for any purpose 
!other than the study of steganography in these protocols. It should not be considered a reliable replacement
!for the libraries distributed with WSJT-X.
!
!
!47 CFR §97 - Rules of the Amateur Radio Service
!
!Subpart A—General Provisions
!
!§97.113 Prohibited transmissions.
!
!(a) No amateur station shall transmit:
!
!(4) Music using a phone emission except as specifically provided elsewhere in this section; communications intended to facilitate a criminal act; messages encoded for the purpose of obscuring their meaning, except as otherwise provided herein; obscene or indecent words or language; or false or deceptive messages, signals or identification.


! Times procedure number n between a call with k=0 (tstart) and with
! k=1 (tstop). Accumulates sums of these times in array ut (user time).
! Also traces all calls (for debugging purposes) if limtrace.gt.0

  character*8 dname

999 return
end subroutine timer
