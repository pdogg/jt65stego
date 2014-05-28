subroutine packpfx(call1,n1,ng,nadd)

  character*12 call1,call0
  character*3 pfx
  logical text

  i1=index(call1,'/')
  if(call1(i1+2:i1+2).eq.' ') then
! Single-character add-on suffix (maybe also fourth suffix letter?)
     call0=call1(:i1-1)
     call packcall(call0,n1,text)
     nadd=1
     nc=ichar(call1(i1+1:i1+1))
     if(nc.ge.48 .and. nc.le.57) then
        n=nc-48
     else if(nc.ge.65 .and. nc.le.90) then
        n=nc-65+10
     else
        n=38
     endif
     nadd=1
     ng=60000-32768+n
  else
! Prefix of 1 to 3 characters
     pfx=call1(:i1-1)
     if(pfx(3:3).eq.' ') pfx=' '//pfx
     if(pfx(3:3).eq.' ') pfx=' '//pfx
     call0=call1(i1+1:)
     call packcall(call0,n1,text)

     ng=0
     do i=1,3
        nc=ichar(pfx(i:i))
        if(nc.ge.48 .and. nc.le.57) then
           n=nc-48
        else if(nc.ge.65 .and. nc.le.90) then
           n=nc-65+10
        else
           n=36
        endif
        ng=37*ng + n
     enddo
     nadd=0
     if(ng.ge.32768) then
        ng=ng-32768
        nadd=1
     endif
  endif

  return
end subroutine packpfx
