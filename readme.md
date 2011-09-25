# NDAR to REDCAP instrument conversion

Created by Rich Stoner, UCSD Autism Center of Excellence
Initial release: September 25th, 2011

## About

This project provides a basic conversion utility from the NDAR data dictionary format into a REDCap instrument. 


## Basic Usage

1. Download the source code or clone the github repository to a local directory.
2. Select the NDAR instruments from the NDAR_library_backup folder and place into the ndardata folder
3. Run the python script to generate a csv from converted NDAR instruments

  python ndar_rosetta.py
  
4. Upload the data dictionary to a REDCap project. A few warnings will appear regarding field name and length.


## Settings

A few options are availble within the ndar_rosetta.py script:

download_files_from_ndar : if true, will download csv files from NDAR site

enable_dropdown_details : if true, will attempt to fix in dropdown details with descriptive text

outputfilename : filename of csv file to be uploaded

