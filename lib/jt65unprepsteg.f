        subroutine unprepsteg(sentups,recdups)

Cf2py intent(in) sentups
Cf2py intent(inout) recdups
	        integer sentups(20),eraups(51),recdups(12)
	        call rs_stegdecode(sentups,eraups,0,recdups,nerr)
	        return
		 end

