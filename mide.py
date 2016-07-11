#!usr/bin/python
# -*- coding: cp1252 -*-
import usbtmc as u
try:
	dvm=u.Instrument("USB::0x0957::0x0607::INSTR")
except: # x cualquier  excepcion
	print "No se pudo encontrar el multímetro"
	raise
else:
	dvm_id=dvm.ask("*IDN?")
	print dvm_id

t=0
for i in range(3):
        dvm.ask("MEAS:VOLT:DC?")
        t=t+float(dvm.ask("READ?"))
print t/3.
