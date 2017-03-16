#!/bin/ksh
#folderdate=$(date +"%Y%m%d")
#echo $folderdate
#echo "python ndfd_solar_pull.py"
#filename="/metero/morningscripts/solar/proxy.txt"
#http_proxy=$(cat "$filename")

#export $http_proxy
#echo $http_proxy
#roswell  104.459328 33.454517
#chaves  104.43944 33.441325
#commanche 104.569833 38.211722 pi tag PSC.COMA.230kV_GEN_MW

#to include additional solar forecast sights add location '-lon -xxx.xxx yy.yyyy'
# to the end current locations in the 'wgrib; calls
~/anaconda3/bin/python3 /metero/morningscripts/solar/ndfd_solar_pull_parse.py
# the solar_pull will grab the 2 binary grib2 files for the conus
#
# wgrib2 will grab the sky cover for each designated location
#  if muliple locations are included this will append to the end with a second ':lat lon value'
# below is an example of the format
# i.e. "1:80:vt=2016072012:lon=254.124717,lat=37.741091,val=44:lon=255.436578,lat=38.220525,val=26"
  
#wgrib2 /metero/morningscripts/solar/ds.sky1.bin -vt -lon -103.85787 33.13295 -lon -105.88 37.74 -lon -104.569833 38.211722> /metero/morningscripts/solar/SPS_solar1.txt
#wgrib2 /metero/morningscripts/solar/ds.sky2.bin -vt -lon -103.85787 33.13295 -lon -105.88 33.74 -lon -104.569833 38.211722> /metero/morningscripts/solar/SPS_solar2.txt
#wgrib2 /metero/morningscripts/solar/ds.sky1.bin -vt -lon -105.88 37.74 -lon -104.569833 38.211722> /metero/morningscripts/solar/PSCO_solar1.txt
#wgrib2 /metero/morningscripts/solar/ds.sky2.bin -vt -lon -105.88 33.74 -lon -104.569833 38.211722> /metero/morningscripts/solar/PSCO_solar2.txt
#cat /metero/morningscripts/solar/PSCO_solar1.txt /metero/morningscripts/solar/PSCO_solar2.txt > /metero/morningscripts/solar/PSCO_solar.txt
#cat /metero/morningscripts/solar/SPS_solar1.txt /metero/morningscripts/solar/SPS_solar2.txt > /metero/morningscripts/solar/SPS_solar.txt

# This parse command program will take the values and remove the un-needed data and reformat
#~/anaconda3/bin/python3 /metero/morningscripts/solar/ndfd_solar_parse.py
#array=(SPS_solar1.txt SPS_solar2.txt SPS_solar.txt PSCO_solar1.txt PSCO_solar2.txt PSCO_solar.txt ds.sky1.bin ds.sky2.bin)
#array()
#for i in "${array[@]}"
#    do
#    j = "/metero/morningscripts/"
#    k = $j$i
#    echo $k
#    if [ -f $k ] ; then
#        rm $k
#    fi
#    done

