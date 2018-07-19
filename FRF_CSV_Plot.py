## Script to plot a single profile line from csv file
## Needs Line
File_Dir ="E:/FRF_GRASS_Analysis/Surveys_For_Analysis/Annual_Set"
#File_List = os.listdir(File_Dir)

Line = 1097

import os
from matplotlib import pyplot as plt
import pandas as pd
survey_Dates = []

#def frf_profile_plot(File_Dir,Line):
File_List = os.listdir(File_Dir)
for f in File_List:
    parts = f.split('_')
    datenumber = parts[1]
    year = datenumber[0:4]
    survey_Dates.append(datenumber)
numberYears = [int(i) for i in survey_Dates]
maxyear = max(numberYears)
minyear = min(numberYears)
totalyears = maxyear - minyear

for file in File_List:
    t = pd.read_csv(File_Dir + "/" + file,header=None)
    plotter = t[t[1] == Line]
    plt.plot(plotter[7],plotter[9], linewidth=2.0)
    del plotter
    del t

words = "Survey Line = {0} ".format(Line)
plt.title(str(words))
plt.xlabel('Distance (m)')
plt.ylabel('Elevation (m)')
plt.rcParams.update({'font.size':10})
plt.legend(survey_Dates)

