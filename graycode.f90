subroutine graycode(dat,n,idir)
!f2py intent(inout) dat

  integer dat(n)
  do i=1,n
     dat(i)=igray(dat(i),idir)
  enddo

  return
end subroutine graycode

