import grass.script as grass
import os



# setup variable holding the raster files
rastFiles = os.listdir("C:/Users/u4hcvmff/Documents/grassdata/North_Carolina/FRF_Annual_NewMask/hist")

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

