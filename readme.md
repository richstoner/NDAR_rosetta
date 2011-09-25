# NDAR to REDCAP instrument conversion

Created by Rich Stoner, UCSD Autism Center of Excellence

Initial release: September 25th, 2011

This project provides a basic conversion utility from the NDAR data dictionary format into a REDCap instrument. 

**Requirements:** Python 2.6+

**Useful links**

* NDAR http://ndar.nih.gov
* NDAR Data dictionary http://ndar.nih.gov/ndarpublicweb/DataStructures.go
* REDCap http://www.project-redcap.org/
* REDCap shared library http://www.project-redcap.org/library/index.php

## Basic Usage

1. Download the source code or clone the github repository to a local directory.
2. Select the NDAR instruments from the NDAR_library_backup folder and place into the ndardata folder
3. Run the python script to generate a csv from converted NDAR instruments

<pre>python ndar_rosetta.py</pre>

  
4. Upload the data dictionary to a REDCap project. A few warnings will appear regarding field name and length.


## Settings

A few options are availble within the ndar_rosetta.py script:

**download_files_from_ndar** : if true, will download csv files from NDAR site

**enable_dropdown_details** : if true, will attempt to fix in dropdown details with descriptive text

**outputfilename** : filename of csv file to be uploaded


## License

**MIT**

Copyright (c) 2011 Rich Stoner

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

