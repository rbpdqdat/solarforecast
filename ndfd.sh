#!/bin/ksh

#to include additional solar forecast sights add location '-lon -xxx.xxx yy.yyyy'
# to the end current locations in the 'wgrib; calls
python3 ndfd_solar_pull_parse.py
# the solar_pull will grab the 2 binary grib2 files for the conus
#

