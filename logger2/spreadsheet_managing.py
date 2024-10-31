#goals: we want to write each data point to a spreadsheet stored locally, then every n minutes we want to upload it to Google Drive, similar to Madi's construction

#obviously it'd be nice if the collector could be the girl storing everything locally but this kinda defeats the "locality",
#and making the Collector do a whole bunch of .csv management to shove everything into one spreadsheet before pushing to Google Drive might be kinda cringe
#so I think we're just going to have to have each Pi push to its own folder in the Google Drive

#in terms of managing the "when to start a new spreadsheet" question, I'd think that we can do the following
#choose a naming convention that includes the date
#before writing, check that the file with such a name exists; if it does, great, write to it; if it doesn't, create it and write to it
#store the name in some sort of global "filename"

from datetime import date
import os
import csv
import shutil

#import numpy as np

def write_locally(point, fields, source_path_stem, header_flag):

    #point will already be pre-formatted, ready to go for a csv
    #I think we should just write .csvs to the drive; it's not like we lose a whole bunch of functionality doing this and it keeps everything as low-maintenance as possible
    
    #if file at path is empty, write headers
    #else write datars only

    now = date.today()
    path = source_path_stem + date.isoformat(now) + ".csv"

    #checking that the file exists is unnecessary, I think :)
    #need to sort out path vs filenames

    with open(path, 'a+', newline='') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fields)

        if header_flag:
            writer.writeheader()

        # writing data rows
        writer.writerows(point)

    header_flag = False;

    return header_flag, path, now
 
    #yeehaw?

def push_to_drive(source_path_stem, now, destination_path_stem):

    #for setting up the Drive,
    #https://forums.raspberrypi.com/viewtopic.php?t=335856

    #for writing,

    destination_path = destination_path_stem + date.isoformat(now) + r'.csv'
    source_path = source_path_stem + date.isoformat(now) + r'.csv'

    '''if not os.path.exists(destination_path):
        os.makedirs(os.path.join(destination_path))'''

    if os.path.exists(source_path):
        shutil.copyfile(source_path, destination_path)
        print("pushed to drive")
    else:
        print("source path does not exist!")

'''filename_stem = "csv_test_"

fields = ["time","temperature","happiness rating"]

point1 = [{"time":"12:41","temperature":70,"happiness rating":8}]
point2 = [{"time":"12:42","temperature":69,"happiness rating":8}]

header_flag = True

for i in np.arange(5):

    header_flag, filename = write_locally(point1, fields, filename_stem, header_flag)'''
