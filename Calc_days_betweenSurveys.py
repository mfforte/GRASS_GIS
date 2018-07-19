import os
import datetime
import numpy as np

fileDir = os.listdir("E:/FRF_GRASS_Analysis/North_4line_allProfiles")
surveyDateList = []

for file in fileDir:
    if file.endswith('.csv'):
        fparts = file.split('_')
        surveyDateList.append(fparts[1])


#dates_nums = [int(i)for i in surveyDateList]
delta_list = []

#dates = (datetime.datetime.strptime(ts,'%Y%m%d')for ts in surveyDateList)



for number in surveyDateList:
    mdate1 = datetime.datetime.strptime(number,"%Y%m%d").date()
    mdate = str(mdate1)
    delta_list.append(mdate1)

surveyDiff = np.diff(delta_list)

Diff_Days = []
for zz in surveyDiff:
    Diff_Days.append(zz.days)

Days_mean = np.mean(Diff_Days)
Days_max = np.max(Diff_Days)
Days_min = np.min(Diff_Days)
Days_std = np.std(Diff_Days)

print ('Mean Difference between Surveys in Days: {} '.format(Days_mean))
print ('Standard Deviation of Days: {} '.format(Days_std))













