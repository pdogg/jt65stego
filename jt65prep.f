	subroutine prepmsg(dgenp,sentp)
Cf2py intent(in) dgenp
Cf2py intent(inout) sentp

	integer dgenp(12),sentp(63)
Ccall rs_init                            !Initialize RS encoder
	call rs_encode(dgenp,sentp)               !RS encode  
	call interleave63(sentp,1)               !Interleave channel symbols
	call graycode(sentp,63,1)
	return
	end
	
C	subroutine callrsinit()
C	
C	call rs_init
C	return
C	end

