#!usr/bin/python
# -*- coding: cp1252 -*-
import usbtmc as u
import sys
try:
        tek=u.Instrument("USB::0x0699::0x036a::INSTR")
	#dvm=u.Instrument("USB::0x0957::0x0607::INSTR")
        #osc=u.Instrument("USB::0x049f::0x505a::INSTR")
	##gen=u.Instrument(0x1ab1,0x0640)
except: # x cualquier  excepcion
	print "No se pudo encontrar el Osciloscopio"
	sys.exit(-1)
	
else:
	tek_id=tek.ask("*IDN?")
	print tek_id

##t=0
##for i in range(3):
##        dvm.ask("MEAS:VOLT:DC?")
##        t=t+float(dvm.ask("READ?"))
##print t/3.
