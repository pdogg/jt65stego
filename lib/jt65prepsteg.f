        subroutine prepsteg(dgenps,sentps)
Cf2py intent(in) dgenps
Cf2py intent(inout) sentps

        integer dgenps(12),sentps(20)
        call rs_stegencode(dgenps,sentps)               !RS encode  
        return
	 end


