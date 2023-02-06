"""!@file computerPlotting.py
@brief      Receives data from a serial port and produces a plot.
@details    When run, this file opens up serial port and receives data from an
            external program running some sort of data collection. After the 
            data transmission ends, the data is plotted and the program ends.
@author     Nathan Dodd
@author     Lewis Kanagy
@author     Sean Wahl
@date       February 7, 2023
"""

# Import the necessary modules for this file.
import serial
from matplotlib import pyplot
   
## The list of x-values for the produced plot.
X = []
## The list of y-values for the produced plot.
Y = []

## The state in which data is read, up to an error in transmission.
S1_READ  = 1
## The state in which the data is graphed.
S2_GRAPH = 2

## The state that the program is currently in.
state = S1_READ

## The serial port object on which data is received.
with serial.Serial ('COM5', 115200) as s_port:

    while True:
        if state == S1_READ:
            # Read lines from the serial port and try to convert them to usable floats.
            try:
                ## A line read from the serial port.
                line = s_port.readline()
                ## The line read, now separated in a list of objects by a comma.
                lineSep = line.split(b',')
                ## The first value in the separated line list.
                potX = lineSep[0].strip()
                ## The second value in the separated line list.
                potY = lineSep[1].strip()
                ## The numerical x-value from the line, in float form.
                x = float(potX)
                ## The numerical y-value from the line, in float form.
                y = float(potY)
            except:
                # If an exception is reached, go to graphing
                #if lineSep == b'done\r\n':
                state = S2_GRAPH
            else:
                # If the data has been processed, append it to a list.
                X.append(x)
                Y.append(y)
                pass
            
        if state == S2_GRAPH:
            # Plot the received data.
            pyplot.plot(X, Y)
            pyplot.xlabel('Time [ms]')
            pyplot.ylabel('Encoder Position [ticks]')
            X = []
            Y = []
            state = S1_READ
            break
        
            
