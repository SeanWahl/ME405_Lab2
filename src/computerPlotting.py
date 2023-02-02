import serial
from matplotlib import pyplot
   
X = []
Y = []

S1_READ  = 1
S2_GRAPH = 2

state = S1_READ

with serial.Serial ('COM5', 115200) as s_port:

    while True:
        if state == S1_READ:
            try:
                line = s_port.readline()
                #print(line)
                lineSep = line.split(b',')
                #print(lineSep)
                potX = lineSep[0].strip()
                potY = lineSep[1].strip()
                x = float(potX)
                y = float(potY)
            except:
                #print("we are in except")
                #if lineSep == b'done\r\n':
                state = S2_GRAPH
            else:
                X.append(x)
                Y.append(y)
                pass
            
        if state == S2_GRAPH:
            #print("we are in graph")
            #print(X)
            #print(Y)
            pyplot.plot(X, Y)
            pyplot.xlabel('Time [ms]')
            pyplot.ylabel('Encoder Position [ticks]')
            X = []
            Y = []
            state = S1_READ
            break
        
            
