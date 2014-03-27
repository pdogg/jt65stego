      subroutine graycode(dat,n,idir)
Cf2py intent(inout) dat
      integer dat(n)
      do i=1,n
         dat(i)=igray(dat(i),idir)
      enddo

      return
      end

