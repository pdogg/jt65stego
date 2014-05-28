      subroutine jt65unpackmsg(dat,msg)
Cf2py intent(inout) msg
Cf2py intent(in) dat
      integer dat(12)
      character msg*22 

      call unpackmsg(dat,msg)
      end
