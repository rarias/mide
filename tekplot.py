#!/usr/bin/python
# tekplot.py v1.0: Takes the binary data extracted via the serial interface
# from the file argument passed and plots using matlib. It's a quick 
# visualization tool.
# Modificado 2019-03-29 Lee datos ASCII y BINARIOS

import sys, os
import struct
from matplotlib import pyplot

def tek_file_decode(filename, print_wdata=False):
    f=open(filename,'r')
    data=f.read()
    sdata=data.split(';')

    # Each parameter is saved to a variable named as Tek Programming Manual 

    # Data width for the waveform to be transferred. 1 or 2 bytes per point.
    byt_nr=sdata[0]
    print "nro de bytes por punto ", byt_nr

    # Number of bits per waveform point for the waveform to be transferred
    bit_nr=sdata[1]
    print "nro de bits por punto ", bit_nr
    
    # Type of encoding for waveform data transferred
    # ASC specifies ASCII curve data.
    # BIN specifies binary curve data.
    encdg=sdata[2] 
    print "codificacion: ", encdg
    
    # Format of binary data for the waveform to be transferred.
    # RI specifies signed integer data-point representation.
    # RP specifies positive integer data-point representation.
    bn_fmt=sdata[3]
    print bn_fmt
    
    # Which byte of binary waveform data is transmitted
    # first during a waveform data transfer when width(data) or
    # byt_nr is set to 2, or bit_nr is set to 16.
    # LSB selects the least significant byte to be transmitted first.
    # MSB selects the most significant byte to be transmitted first.
    byt_or=sdata[4] 
    print byt_or
    
    # Number of points that are in the transmitted waveform record
    nr_pt=sdata[5] 
    print nr_pt
    
    # Descriptive string from the waveform specified if active (if not returns 2244) 
    # Example: "Ch1, DC coupling, 5.0E0 V/div, 5.0E-6 s/div, 2500 points, Sample mode"
    wfid=sdata[6]  
    if print_wdata == True:
        print wfid

    # Format (Y or ENV) of the reference waveform
    # Y specifies a normal waveform where one ASCII or binary data point
    # is transmitted for each point in the waveform record.
    # xn = xzero + xincr (n - pt_off)
    # yn = yzero + ymult (yn - yoff)
    # ENV specifies that the oscilloscope transmit the waveform as
    # minimum and maximum point pairs. Peak detect waveforms use
    # ENV format. Peak Detect mode specifies a maximum of 1250
    # (minimum, maximum) pairs, with the time between pairs being
    # 2*xincr.
    pt_fmt=sdata[7]  
    print pt_fmt
    
    # Specifies the interval (seconds per point for non-FFT, Hertz per point for 
    # FFT) between samples of the reference waveform.
    xincr=sdata[8]
    print xincr

    # Always 0, unless the DATA:SOUrce waveform is not displayed, 
    # in which case the query generates an error and returns event code 2244.
    pt_off=sdata[9]  
    print pt_off
    
    # The position of the first sample of the waveform
    xzero=sdata[10] 

    # Specifies the horizontal units ("s" for seconds and "Hz" for Hertz)
    xunit=sdata[11]

    # It's a value, expressed in yunits per digitizer level, used to convert 
    # waveform record values to yunit using
    # yn = yzero + ymult (yn - yoff)
    ymult=sdata[12] 

    # It's a value, expressed in yunits, used to convert waveform record 
    # values to yunit values using
    yzero=sdata[13] 

    # It's a value, expressed in digitizer levels, used to convert waveform 
    # record values to yunit values using
    # yn = yzero + ymult (yn - yoff)
    yoff=sdata[14] 

    # The vertical units of the waveform
    yunit=sdata[15] 

    # Waveform data
    # swaveform=sdata[16][6:-1]
    # Hack to solve the problem of extra ; in binary data
    # There are 6 extra bytes at the beginning
    swaveform=";".join(sdata[16:])[6:-1]
    if bn_fmt=="RP":
        wavelist=swaveform.split(',')
        waveform=[]
        for i in wavelist:
            waveform.append(int(i))
        print "nro. de datos en el eje Y: ", len(wavelist)
    else:
        print len(swaveform)
        waveform=struct.unpack('h'*2500,swaveform)
        # 'h' = unsigned short = 16 bits
        # Ver otros formatos en https://docs.python.org/3/library/struct.html
    
    # Convert the data:
    ydata=[float(yzero)+float(ymult)*(float(i)-float(yoff)) for i in waveform]
    xdata=[float(xzero)+float(xincr)*(i-float(pt_off)) for i in range(int(nr_pt)) ]
    f.close()
    if len(ydata)>len(xdata):
        ydata=ydata[1:len(xdata)+1]
        print "recorta datos en Y"
    elif len(xdata)>len(ydata):
        xdata=xdata[1:len(ydata)+1]
        print "recorta datos en X"
    return [xdata,ydata,wfid]

if __name__ == '__main__':
    if len(sys.argv)>1:
        data = tek_file_decode(sys.argv[1], True)
        pyplot.plot(data[0],data[1])
        pyplot.show()
    else:
        print 'Error: Filename argument missing.'

