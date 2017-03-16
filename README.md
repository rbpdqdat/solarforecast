# solarforecast

### Notes:
-**Created on 7/19/2016**
-**Complete Revision: 8/11/2016**

This briefly documents some of the processes included in this folder.

The 'csv' files with the solar names are created from the actual solar output
The data is the max value for the hour during a 10 day rolling period

## Installation

Just copy the code into the appropriate directory and make sure you read the requirements. 

##*Requirements*

This is designed to run on a Linux platform with using Python 3.4.  Other versions may work.  It is also necessary to be install wgrib.  More information about wgrib can be found at the [Climate Prediction Center](http://www.cpc.ncep.noaa.gov/products/wesley/wgrib.html).  The following is a brief description of the files that are included in this repository. 

## Directories:

There are 2 directories needed: *OutputFiles* and *solarDailyMax*.  This keeps things tidy, especially for automated processes that download data each day.  

*OutputFiles:* location where the final solar output by farm is created.

*solarDailyMax:* location where the 10 day rolling average of solar output is created.  These files are needed to create a max hourly profile of solar data and then the cloud cover data from grib files is used to decrease the solar generation.

```ndfd.sh```

This shell script runs the `ndfd_solar_pull_parse.py` program.  

```ndfd_solar_pull_parse.py```

The `ndfd_solar_pull_parse.py` program has a few defined functions to deal with timezones, pulling binary data from NOAA, parsing the data for each specific location, and creating a forecast file for each specified location.  *The solarMeta.csv* file contains the regions, solar array names, and the latitude and longitudes of the farms.  

```solar_max_profile.py```

This python script creates a new solar file from and existing csv file.  These profiles are needed to create an annual daily cycle of solar output. 

# Version and License

v1.1.3 released 1/1/2017 under [MIT](https://choosealicense.com/licenses/mit/) license

# Support and Credits

The solarforecast files were designed as a simple forecast tool for large scale generation projects.  
If you have any questions direct them to rlbigley@me.com.  Some of the code was created in collaboration with
Shane Motley. 
