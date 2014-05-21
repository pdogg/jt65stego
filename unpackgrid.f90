subroutine unpackgrid(ng,grid)

  parameter (NGBASE=180*180)
  character grid*4,grid6*6,digit*10
  data digit/'0123456789'/

  grid='    '
  if(ng.ge.32400) go to 10
  dlat=mod(ng,180)-90
  dlong=(ng/180)*2 - 180 + 2
  call deg2grid(dlong,dlat,grid6)
  grid=grid6(1:4) !XXX explicitly truncate this -db
  go to 100

10 n=ng-NGBASE-1
  if(n.ge.1 .and.n.le.30) then
     grid(1:1)='-'
     grid(2:2)=char(48+n/10)
     grid(3:3)=char(48+mod(n,10))
  else if(n.ge.31 .and.n.le.60) then
     n=n-30
     grid(1:2)='R-'
     grid(3:3)=char(48+n/10)
     grid(4:4)=char(48+mod(n,10))
  else if(n.eq.61) then
     grid='RO'
  else if(n.eq.62) then
     grid='RRR'
  else if(n.eq.63) then
     grid='73'
  endif

100 return
end subroutine unpackgrid

