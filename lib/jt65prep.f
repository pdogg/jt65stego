        subroutine prepmsg(dgenp,sentp)
!f2py intent(in) dgenp
!f2py intent(inout) sentp

        integer dgenp(12),sentp(63)
        call rs_encode(dgenp,sentp)               !RS encode  
        call interleave63(sentp,1)               !Interleave channel symbols
        call graycode(sentp,63,1)
        return
        end
	

