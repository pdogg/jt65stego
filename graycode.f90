!Modified from original WSJT source Copyright Joe Taylor K1JT Release under GPL
!By Paul Drapeau - May 20, 2014

subroutine graycode(dat,n,idir)
!f2py intent(inout) dat

  integer dat(n)
  do i=1,n
     dat(i)=igray(dat(i),idir)
  enddo

  return
end subroutine graycode

