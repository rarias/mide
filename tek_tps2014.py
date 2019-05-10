#! /usr/bin/python
# -*- coding: cp1252 -*-
"""
    Se conecta a un osciloscopio Tektronics a través del puerto serie
    y envia los comando necesarios para obtener la senial de un canal.
    Ultima actualización 2019-05-10 19:21
"""

import serial as s
# El osciloscopio se conecta por puerto serie via un adaptador 232-USB
# marca ATTEN, modelo UC-232A.   El driver se puede bajar del sitio:
# https://www.aten.com/global/en/supportcenter/downloads/?action=display_product&pid=575

import time as t
osc=s.Serial('COM6', baudrate=19200, timeout=2, xonxoff = False)

def LeeLinea( dispo ):
    hay_datos=1
    resp=''
    tope=0
    while( hay_datos and tope<60):
        tope=tope+1
        rta=dispo.read()
        if rta=='':
            hay_datos=0 # no hay respuesta
            print 'no hay respuesta'
        elif rta=='\n':
            hay_datos=0 # fin de un string
        else:
            resp=resp+rta # respuesta en progreso ...
    return resp

def LeeTodo( dispo, nro_bytes ):
    """ Lee la respuesta completa del dispositivo (ver:
        https://stackoverflow.com/questions/19161768/pyserial-inwaiting-returns-incorrect-number-of-bytes)
        Read all characters on the serial port and return them."""
    if not dispo.timeout:
        raise TypeError('El puerto tiene que tener un timeout>0!')
    read_buffer = b''
    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
        byte_chunk = dispo.read(size=nro_bytes)
        read_buffer += byte_chunk
        if not len(byte_chunk) == nro_bytes:
            break

    return read_buffer

    
def comando(puerto, comando):
    puerto.write(comando)
    
def pregunta(puerto, comando):
    puerto.write(comando)
    rta=LeeLinea(puerto)
    return rta
    
if __name__ == '__main__':
    if osc.isOpen():
        osc.flushInput()
        print 'istrumento:', pregunta(osc, '*IDN?\n')
        comando(osc, 'HEADER ON\n')
	
	#print pregunta(osc, 'RS232:BAUD 19200\n')
	#osc.baudrate=19200
	#t.sleep(1)
	#print pregunta(osc, 'RS232:BAUD?\n')
	
        print 'canal activo?', pregunta(osc,'SELECT?\n')
        comando(osc, 'DATA:SOURCE CH1\n') # fija canal 1
        print pregunta(osc, 'DATA:SOURCE?\n')
##    comando(osc, 'DATA:ENCoding ASCII\n') #RIBINARY\n')
        comando(osc, 'DATA:ENCoding RIBINARY\n')
	#print pregunta(osc, 'DATA:ENCODing?\n')
        comando(osc,'DATA:START 1; STOP 2500; ENCD RIBINARY; WIDTH 2\n')
        comando(osc,'HEADER OFF\n')
##    print pregunta(osc, 'WFMPre:PT_Fm?\n')    # pide encabezado
##    t.sleep(1)
##    osc.flush()
	#print pregunta(osc, 'CURVe?\n')     # pide forma de onda
        print pregunta(osc, 'wavfrm?\n')
        t.sleep(1)
        tini=t.time()
        onda=LeeTodo(osc, 256)
        f = open('forma_de_onda.tek', "w")
        f.write(onda)
        f.close()
        print "tiempo de lectura = ", t.time()-tini
        
    else:
        print 'Puerto cerrado'
    osc.close()

