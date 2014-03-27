      program JT65code
C Modified by pdogg - just outputs the channel symbols with FEC
C  Provides examples of message packing, bit and symbol ordering,
C  Reed Solomon encoding, and other necessary details of the JT65
C  protocol.

      character*22 msg0,msg,decoded,cok*3
      integer dgen(12),sent(63),era(51),recd(12)

      nargs=iargc()
      if(nargs.ne.1) then
         print*,'Usage: JT65code "message"'
         go to 999
      endif

      call getarg(1,msg0)                     !Get message from command line
      msg=msg0

c      call chkmsg(msg,cok,nspecial,flip)      !See if it includes "OOO" report
c      if(nspecial.gt.0) then                  !or is a shorthand message
c         write(*,1010) 
c 1010    format('Shorthand message.')
c         go to 999
c      endif

c      call packmsg(msg,dgen)                  !Pack message into 72 bits
c      write(*,1020) msg0
c 1020 format('Message:   ',a22)               !Echo input message
c      if(and(dgen(10),8).ne.0) write(*,1030)  !Is the plain text bit set?
c 1030 format('Plain text.')         
c      write(*,1040) dgen
c 1040 format(12i3) !Display packed symbols

      call packmsg(msg,dgen)                  !Pack user message
      call rs_init                            !Initialize RS encoder
      call rs_encode(dgen,sent)               !RS encode
    
      call interleave63(sent,1)               !Interleave channel symbols
      call graycode(sent,63,1)                !Apply Gray code
c      sent(2:2) = 33
c      sent(6:6) = 1
c      sent(9:9) = 19
c      sent(12:12) = 33
c      sent(15:15) = 12
c      sent(18:18) = 61
c      sent(21:21) = 7
c      sent(22:22) = 23
c      sent(26:26) = 27
c      sent(28:28) = 44
c      sent(30:30) = 27
c      sent(32:32) = 60
      write(*,1050) sent
1050  format(63i3)

c      call graycode(sent,63,-1)
c      call interleave63(sent,-1)
c      call rs_decode(sent,era,0,recd,nerr)
c      call unpackmsg(recd,decoded)            !Unpack the user message
c      write(*,1060) decoded,cok
c 1060 format('Decoded message: ',a22,2x,a3)

 

 999  end
