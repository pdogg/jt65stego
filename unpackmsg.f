      subroutine unpackmsg(dat,msg)
Cf2py intent(inout) msg
Cf2py intent(in) dat
      parameter (NBASE=37*36*10*27*27*27)
      parameter (NGBASE=180*180)
      integer dat(12)
      character c1*12,c2*12,grid*4,msg*22,grid6*6
      logical cqnnn

      cqnnn=.false.
      nc1=lshift(dat(1),22) + lshift(dat(2),16) + lshift(dat(3),10)+
     +  lshift(dat(4),4) + and(rshift(dat(5),2),15)

      nc2=lshift(and(dat(5),3),26) + lshift(dat(6),20) + 
     +  lshift(dat(7),14) + lshift(dat(8),8) + lshift(dat(9),2) + 
     +  and(rshift(dat(10),4),3)

      ng=lshift(and(dat(10),15),12) + lshift(dat(11),6) + dat(12)

      if(ng.gt.32768) then
         call unpacktext(nc1,nc2,ng,msg)
         go to 100
      endif

      if(nc1.lt.NBASE) then
         call unpackcall(nc1,c1)
      else
         c1='......'
         if(nc1.eq.NBASE+1) c1='CQ    '
         if(nc1.eq.NBASE+2) c1='QRZ   '
         nfreq=nc1-NBASE-3
         if(nfreq.ge.0 .and. nfreq.le.999) then
            write(c1,1002) nfreq
 1002       format('CQ ',i3.3)
            cqnnn=.true.
         endif         
      endif

      if(nc2.lt.NBASE) then
         call unpackcall(nc2,c2)
      else
         c2='......'
      endif

      call unpackgrid(ng,grid)
      grid6=grid//'ma'
      call grid2k(grid6,k)
      if(k.ge.1 .and. k.le.450)   call getpfx2(k,c1)
      if(k.ge.451 .and. k.le.900) call getpfx2(k,c2)

      i=index(c1,char(0))
      if(i.ge.3) c1=c1(1:i-1)//'            '
      i=index(c2,char(0))
      if(i.ge.3) c2=c2(1:i-1)//'            '

      msg='                      '
      j=0
      if(cqnnn) then
         msg=c1//'                '
         j=7                                  !### ??? ###
         go to 10
      endif

      do i=1,12
         j=j+1
         msg(j:j)=c1(i:i)
         if(c1(i:i).eq.' ') go to 10
      enddo
      j=j+1
      msg(j:j)=' '

 10   do i=1,12
         if(j.le.21) j=j+1
         msg(j:j)=c2(i:i)
         if(c2(i:i).eq.' ') go to 20
      enddo
      msg(j:j)=' '

 20   if(k.eq.0) then
         do i=1,4
            if(j.le.21) j=j+1
            msg(j:j)=grid(i:i)
         enddo
         j=j+1
         msg(j:j)=' '
      endif

 100  return
      end
