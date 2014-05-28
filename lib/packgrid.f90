subroutine packgrid(grid,ng,text)

  parameter (NGBASE=180*180)
  character*4 grid
  logical text

  text=.false.
  if(grid.eq.'    ') go to 90                 !Blank grid is OK

! Test for numerical signal report, etc.
  if(grid(1:1).eq.'-') then
     if(grid(3:3).ne.' ') then
        n=10*(ichar(grid(2:2))-48) + ichar(grid(3:3)) - 48
     else
        n=ichar(grid(2:2))-48
     endif
     if(n.gt.30) n=30
     ng=NGBASE+1+n
     go to 100
  else if(grid(1:2).eq.'R-') then
     if(grid(4:4).ne.' ') then
        n=10*(ichar(grid(3:3))-48) + ichar(grid(4:4)) - 48
     else
        n=ichar(grid(3:3))-48
     endif
     if(n.gt.30) n=30
     if(n.eq.0) go to 90
     ng=NGBASE+31+n
     go to 100
  else if(grid(1:2).eq.'RO') then
     ng=NGBASE+62
     go to 100
  else if(grid(1:3).eq.'RRR') then
     ng=NGBASE+63
     go to 100
  else if(grid(1:2).eq.'73') then
     ng=NGBASE+64
     go to 100
  endif

  if(grid(1:1).lt.'A' .or. grid(1:1).gt.'R') text=.true.
  if(grid(2:2).lt.'A' .or. grid(2:2).gt.'R') text=.true.
  if(grid(3:3).lt.'0' .or. grid(3:3).gt.'9') text=.true.
  if(grid(4:4).lt.'0' .or. grid(4:4).gt.'9') text=.true.
  if(text) go to 100

  call grid2deg(grid//'mm',dlong,dlat)
  long=dlong
  lat=dlat+ 90.0
  ng=((long+180)/2)*180 + lat
  go to 100

90 ng=NGBASE + 1

100 return
end subroutine packgrid

