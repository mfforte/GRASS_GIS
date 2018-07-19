# Forte - November 2017

# GRASS script for raster based time series analysis of FRF survey data

# 1. read in FRF csv survey files convert to vector points
# 2. run interpolation
# 3. run raster time series analysis

import grass.script as grass
import os

# setup file locations
fileHome = "E:/FRF_GRASS_Analysis/Annual_Set"
fileDir = os.listdir("E:/FRF_GRASS_Analysis/Annual_Set")
outputDir = "E:/FRF_GRASS_Analysis/GRASS_Processing"


# call v.in.ascii to read in survey points [currently set to state plane columns 6,7]
# need to remember to drop .csv off during file output - not allowed.

for file in fileDir:

    if file.endswith('.csv'):

        grass.run_command('v.in.ascii', input= os.path.join(fileHome,file), output= "v_pts_" +file[0:12],separator=',', x=6, y=7, z=10, overwrite=True)


# Interpolation
grass.run_command('g.region',res=4)
vecFiles = os.listdir("C:/Users/u4hcvmff/Documents/grassdata/North_Carolina/FRF_Annual_Dune/vector")
for file in vecFiles:
    if file.startswith('v_'):
        #grass.run_command('v.surf.rst', input=file, elev=file + 'elev', slope=file + 'slope', tension=40, smooth=5, theta=100, scalex=0.14, overwrite=True)
        grass.run_command('v.surf.rst', input=file, elev=file + 'elev', slope=file + 'slope', tension=40, smooth=5, overwrite=True)


# setup variable holding the raster files
rastFiles = os.listdir("C:/Users/u4hcvmff/Documents/grassdata/North_Carolina/FRF_Annual_Dune/hist")

# Create Lists from slope and elevation files for use in r.series
s_list = []
e_list = []
for i in rastFiles:
    if i.endswith('slope'):
        s_list.append(i)
    elif i.endswith('elev'):
        e_list.append(i)


# setup rules files (dates) and color specifications for outputs
r_fname = 'C:/Users/u4hcvmff/Documents/grassdata/North_Carolina/FRF_Annual/rules.txt'
cslope_fname = 'C:/Users/u4hcvmff/Documents/grassdata/North_Carolina/FRF_Annual/regr_slope_slopeData_color.txt'
celev_fname = 'C:/Users/u4hcvmff/Documents/grassdata/North_Carolina/FRF_Annual/regr_slope_elevationData_color.txt'

# running r.series accessing two lists created above

#grass.run_command('r.series',input=e_list,output='FRF_std', method='stddev', output='FRF_diff_r',method='range', overwrite=True)
grass.run_command('r.series',input=e_list,output='FRF_r_s_Dune,FRF_r_o_Dune,FRF_r_c_Dune',method='slope,offset,detcoeff', overwrite=True)
grass.run_command('r.colors',map='FRF_r_s',rules=celev_fname)
grass.run_command('r.series',input=s_list,output='FRF_r_s_slp_Dune,FRF_r_o_slp_Dune,FRF_r_c_slp_Dune',method='slope,offset,detcoeff', overwrite=True)
grass.run_command('r.colors',map='FRF_r_s_slp',rules=cslope_fname)
#grass.run_command('r.series',input=e_list,output='FRF_min_time',method='min_raster',overwrite=True)
#grass.run_command('r.series',input=e_list,output='FRF_max_time',method='max_raster',overwrite=True)
#grass.run_command('r.category',map='FRF_min_time', rules=r_fname)
#grass.run_command('r.category',mape='FRF_max_time', rules=r_fname)