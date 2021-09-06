#Aryan Sidana
#400232302
#Python 3.8.8
#Matplotlib, numpy, serial, math libraries needed

import serial
import numpy as np
import math
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
#Modify the following line with your own serial port details
#   Currently set COM3 as serial port at 115.2kbps 8N1
#   Refer to PySerial API for other options.  One option to consider is
#   the "timeout" - allowing the program to proceed if after a defined
#   timeout period.  The default = 0, which means wait forever.


s = serial.Serial("COM4", 115200) #Set Com port and buad rate

print("Opening: " + s.name)
Tdata=[]
data=[]
y=0
count=0

for j in range(10): #Repeat for 10 measurments
    data=[]
    for i in range(64): #Read all 64 measurment data points   
        x = s.readline()
        c = x.decode()     # convert byte type to str
        if(c!='check for data ready done.\r\n'):
            data.append(int(c)) #Add data point to array
            print(int(c))
    Tdata.append(data) #add plane array to list of arrays
    print("Done Measurement #"+str(j+1))

print("Done All Measurements")


print("Closing: " + s.name) #close serial port
s.close();

xlist=[]
arr=[]

#Create arrays of x values, with delta of 100 mm
for j in range(10):
    arr=[(j*100) for i in range(64)]
    xlist.append(arr)
ylist=[]
zlist=[]
y=[]
z=[]
if(len(Tdata[0])==63):
    Tdata[0].append(Tdata[0][62])

#create array of angles, 0-360 increments of 5.625 degrees
angle=np.linspace(0,360,64,False,False,int)
#print(angle)
#print(Tdata)

#For all the data points on the list of arrays, use th angle and distance to convert to y,z values
for dis in Tdata:
    i=0
    z=[]
    y=[]
    for d in dis:
        y.append(d*math.cos(math.radians((angle[i])))) #y = distance*cos(angle)
        z.append(d*math.sin(math.radians((angle[i])))) #z = distance*sin(angle)
        i=i+1
    ylist.append(y)
    zlist.append(z)

#print(ylist)
#print(zlist)
#print(xlist)

#Add an extra point to each y-z plane to make sure the plots connect
for i in range(10):
    xlist[i].append(xlist[i][0])
    ylist[i].append(ylist[i][0])
    zlist[i].append(zlist[i][0])

#Create raw data file
file1 = open('xyz.txt', 'w')

#add all x,y,z points to raw data file
for j in range(10):
    for i in range(64):
        file1.write(str(xlist[j][i])+" " + str(ylist[j][i])+" " + str(zlist[j][i]))
        file1.write("\n")
file1.close()

#Create 3D render
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

#Plot all y-z planes as sepreate plots on 3D render
for i in range(0,10):
    ax.plot(xlist[i], zlist[i], ylist[i], color="red")

#Add axis labels
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")

ax.view_init(elev=-170, azim=-130)

plt.show()

