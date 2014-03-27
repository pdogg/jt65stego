      subroutine getpfx2(k0,callsign)

      character callsign*12
      include 'pfx.f'

      k=k0
      if(k.gt.450) k=k-450
      if(k.ge.1 .and. k.le.NZ) then
         iz=index(pfx(k),' ') - 1
         callsign=pfx(k)(1:iz)//'/'//callsign
         go to 10
      else if(k.ge.401 .and. k.le.411) then
         iz=index(callsign,' ') - 1
         callsign=callsign(1:iz)//'/'//sfx(k-400)
      endif
     
 10   return
      end

