subroutine extract(s3,nadd,ncount,nhist,decoded,ltext,nbmkv)

!This library is derived from the JT65/JT9 etc. library released under GPL as part of the WSJT-X source
!originally authored by Joe Taylor K1JT and available from: http://www.physics.princeton.edu/pulsar/K1JT/devel.html!
!Many files have been modified for use in the JT65Stego project in May/June of 2014 by
!Paul Drapeau and Brent Dukes and this version of the library should not be used for any purpose 
!other than the study of steganography in these protocols. It should not be considered a reliable replacement
!for the libraries distributed with WSJT-X.
!
!
!47 CFR §97 - Rules of the Amateur Radio Service
!
!Subpart A—General Provisions
!
!§97.113 Prohibited transmissions.
!
!(a) No amateur station shall transmit:
!
!(4) Music using a phone emission except as specifically provided elsewhere in this section; communications intended to facilitate a criminal act; messages encoded for the purpose of obscuring their meaning, except as otherwise provided herein; obscene or indecent words or language; or false or deceptive messages, signals or identification.  real s3(64,63)
  character decoded*22
  integer era(51),dat4(12),indx(64)
  integer mrsym(63),mr2sym(63),mrprob(63),mr2prob(63),mrprobsave(63),mrsymsave(63)
  logical nokv,ltext
  data nokv/.false./,nsec1/0/
  save

  nbmkv=0
  nfail=0
1 continue
  call demod64a(s3,nadd,mrsym,mrprob,mr2sym,mr2prob,ntest,nlow)
  if(ntest.lt.50 .or. nlow.gt.20) then
     ncount=-999                         !Flag bad data
     go to 900
  endif
  call chkhist(mrsym,nhist,ipk)

  if(nhist.ge.20) then
     nfail=nfail+1
     call pctile(s3,4032,50,base)     ! ### or, use ave from demod64a
     do j=1,63
        s3(ipk,j)=base
     enddo
     if(nfail.gt.30) then
        decoded='                      '
        ncount=-1
        go to 900
     endif
     go to 1
  endif
!pdogg - save arrays incase we need them (incase good decode)
  mrsymsave=mrsym
  mrprobsave=mrprob
  call graycode65(mrsym,63,-1)
  call interleave63(mrsym,-1)
  call interleave63(mrprob,-1)

! Decode using Berlekamp-Massey algorithm
  nemax=30                                         !Max BM erasures
  call indexx(63,mrprob,indx)
  do i=1,nemax
     j=indx(i)
     if(mrprob(j).gt.120) then
        ne2=i-1
        go to 2
     endif
     era(i)=j-1
  enddo
  ne2=nemax
2 decoded='                      '
  do nerase=0,ne2,2
     call rs_decode(mrsym,era,nerase,dat4,ncount)
     if(ncount.ge.0) then
        write(*,1776) mrsymsave
1776 format(63i3)
        write(*,1984) mrprobsave
1984 format(63i4) 
        call unpackmsg(dat4,decoded)
        if(iand(dat4(10),8).ne.0) ltext=.true.
        nbmkv=1
        go to 900
     endif
  enddo

! Berlekamp-Massey algorithm failed, try Koetter-Vardy
!pdogg - stop calling kvasd for now!!! <<XXX>>
 go to 900

  maxe=8                             !Max KV errors in 12 most reliable symbols
!  xlambda=12.0
  xlambda=7.99
  call graycode65(mr2sym,63,-1)
  call interleave63(mr2sym,-1)
  call interleave63(mr2prob,-1)

  nsec1=nsec1+1
  write(22,rec=1) nsec1,xlambda,maxe,200,mrsym,mrprob,mr2sym,mr2prob
  call flush(22)
!  call timer('kvasd   ',0)
#ifdef UNIX
!  iret=system('./kvasd -q > dev_null')
#else
!  iret=system('kvasd -q > dev_null')
#endif
!  call timer('kvasd   ',1)
!  if(iret.ne.0) then
!     if(.not.nokv) write(*,1000) iret
!1000 format('Error in KV decoder, or no KV decoder present.',i12)
     nokv=.true.
     go to 900
!  endif

  read(22,rec=2,err=900) nsec2,ncount,dat4
  j=nsec2                !Silence compiler warning
  decoded='                      '
  ltext=.false.
  if(ncount.ge.0) then
     call unpackmsg(dat4,decoded)     !Unpack the user message
     if(index(decoded,'...... ').gt.0) then
        ncount=-1
        go to 900
     endif
     if(iand(dat4(10),8).ne.0) ltext=.true.
     nbmkv=2
  endif

900 continue

  return
end subroutine extract
