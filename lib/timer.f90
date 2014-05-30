subroutine timer(dname,k)
! made this a do nothing function to get temp performance improvement in ./jt65

! Times procedure number n between a call with k=0 (tstart) and with
! k=1 (tstop). Accumulates sums of these times in array ut (user time).
! Also traces all calls (for debugging purposes) if limtrace.gt.0

  character*8 dname

999 return
end subroutine timer
