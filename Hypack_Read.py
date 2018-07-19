# script to read hypack raw file and extract the POS position line containing easting, northing, and elevation (tide)
# writes data to a file comma separated in the format [902464.015,48713.648,3.452]
# mainly used to for comparing hypack RTK positions with post processed positions
import numpy as np
import os
from matplotlib import pyplot as plt

File_Dir ="C:/FRF_Survey/Python_Hypack/Data/"
file_outName = File_Dir + "XYZT_GPS.txt"
gpsFile = "C:/FRF_Survey/Python_Hypack/Data/frf traj test nc sp old nad83.txt"
file_outName_post = File_Dir + "XYZT_PostProcess.txt"

# create empty variables for hypack files
X = []
Y = []
Z = []
g_Time = []
#create empty variables for post processed file
X_post = []
Y_post = []
Z_post = []
T_post = []

for filename in os.listdir(File_Dir):
    if filename.endswith(".RAW"):
        with open (File_Dir + filename,"rb") as f:
# read through hypack text file extracting X,Y,Z and appending
            for line in f:
                if line.startswith("POS"):
                    pos = line.split()
                    if len(pos)==6:
                        X.append(float(pos[3]))
                        Y.append(float(pos[4]))
                        Z.append(float(pos[5]))

                if line.startswith("MSG"):
                    gps_time = line.split()
                    gps_timet = gps_time[3].split(',')
                    g_Time.append(float(gps_timet[2]))



f.close()


with open(gpsFile,"rb") as c:
    for line in c:
        gpsT = line.split()
        tpart = gpsT[5]
        T_part = tpart.replace(':','')
        X_post.append(float(gpsT[1]))
        Y_post.append(float(gpsT[2]))
        Z_post.append(float(gpsT[3]))
        T_post.append(float(T_part))

c.close()


# to ensure the arrays are same length - hypack files sometimes have more lines than others
g_Time = g_Time[:len(X)]

# converting to numpy arrays for obtaining indices using in 1d
T_post = np.array(T_post, dtype=np.float)
g_Time = np.array(g_Time)
X_post = np.array(X_post,dtype=np.float)
Y_post = np.array(Y_post,dtype=np.float)
Z_post = np.array(Z_post,dtype=np.float)



# find indexs of interest for T_post
T_postInds= np.argwhere(np.in1d(T_post, g_Time)).squeeze()  # produces a True/False array for matches of T_post
g_timeInds = np.argwhere(np.in1d(g_Time, T_post)).squeeze()  # produces a True/false array for matches of gtime

# extract each of the variables using the indices
goodT_post = T_post[T_postInds]  # pull the good indices found above
goodG_time = g_Time[g_timeInds]  # pull good indx from gtime
goodX_post = X_post[T_postInds]
goodY_post = Y_post[T_postInds]
goodZ_post = Z_post[T_postInds]




# numpy work - rearrange variables into column arrays
a = np.column_stack((goodX_post,goodY_post,goodZ_post,goodT_post))
b = np.column_stack((X,Y,Z,g_Time))

# sorting on time column
a = a[a[:,3].argsort()]
b = b[b[:,3].argsort()]


z_diff = a[1:100,2] - b[1:100,2]+0.07 # added 7cm to adjust for possible phase center offset
z_mean = np.mean(z_diff)
z_deviation = np.std(z_diff)
print "The mean = {} and standard deviation = {}".format(z_mean,z_deviation)

# make plot to ensure validity
#fig, ax = plt.subplots()
plt.subplot(2,1,1)
plt.plot(a[1:100,3],a[1:100,2],'.',label='Post')
plt.plot(b[3:103,3],b[3:103,2],'.',label= 'RTK')
plt.title('RTK GPS vs Post Processed GPS')
plt.xlabel('')
plt.ylabel('Elevation m')
plt.legend()

plt.subplot(2,1,2)
plt.plot(b[1:100,3],z_diff,'.')
#plt.plot([140000, 144500], [0,0], 'k-')
plt.ylabel('Elevation Difference m')
plt.xlabel('Time UTC')
plt.show()



# write file
np.savetxt(file_outName,b,delimiter=",",fmt='%1.3f')
np.savetxt(file_outName_post,a,delimiter=",",fmt='%1.3f')



