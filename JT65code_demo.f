      program JT65code
C Modified by pdogg
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

      call chkmsg(msg,cok,nspecial,flip)      !See if it includes "OOO" report
      if(nspecial.gt.0) then                  !or is a shorthand message
         write(*,1010) 
 1010    format('Shorthand message.')
         go to 999
      endif

      call packmsg(msg,dgen)                  !Pack message into 72 bits
      write(*,1020) msg0
 1020 format('Message:   ',a22)               !Echo input message
      if(and(dgen(10),8).ne.0) write(*,1030)  !Is the plain text bit set?
 1030 format('Plain text.')         
      write(*,1040) dgen
 1040 format('Packed message, 6-bit symbols: ',12i3) !Display packed symbols

      call packmsg(msg,dgen)                  !Pack user message
      call rs_init                            !Initialize RS encoder
      call rs_encode(dgen,sent)               !RS encode
    
      call interleave63(sent,1)               !Interleave channel symbols
      call graycode(sent,63,1)                !Apply Gray code
      sent(2:2) = 33
      sent(6:6) = 1
      sent(9:9) = 19
      sent(12:12) = 33
      sent(15:15) = 12
      sent(18:18) = 61
      sent(21:21) = 7
      sent(22:22) = 23
      sent(26:26) = 27
      sent(28:28) = 44
      sent(30:30) = 27
      sent(32:32) = 60
      write(*,1050) sent
 1050 format('Channel symbols, including FEC:'/(i5,20i3))

      call graycode(sent,63,-1)
      call interleave63(sent,-1)
      call rs_decode(sent,era,0,recd,nerr)
      call unpackmsg(recd,decoded)            !Unpack the user message
      write(*,1060) decoded,cok
 1060 format('Decoded message: ',a22,2x,a3)

 

 999  end
