import os


fileDir = os.listdir("E:/FRF_GRASS_Analysis/Surveys_For_Analysis")

for file in fileDir:
    if file.endswith('.csv'):
        parts = file.split('_')
        date = parts[1]
        year = date[0:4]
        month = date[4:6]
        day = date[6:9]
        finalDate = date
        os.rename(file,'s_' + year +".csv")







