	subroutine unprepmsg(sentup,recdup)

Cf2py intent(in) sentup
Cf2py intent(inout) recdup

	integer sentup(63),eraup(51),recdup(12)
C	call rs_init
	call graycode(sentup,63,-1)
	call interleave63(sentup,-1)
	call rs_decode(sentup,eraup,0,recdup,nerr)
	return
	end
