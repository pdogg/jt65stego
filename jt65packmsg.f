      subroutine jt65packmsg(msg,dat)
Cf2py intent(in) msg
Cf2py intent(inout) dat
      character*22 msg
      integer dat(12)

      call packmsg(msg,dat)
      end
