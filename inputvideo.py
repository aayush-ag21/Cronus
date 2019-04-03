import os
for i in range(100,1000): 


    os.system("raspivid -o /home/pi/cctv/input%3d.h264 -t 10000"  % (i))



