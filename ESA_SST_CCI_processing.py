
"""
########################################
# ESA CCI SST Processing
#
# Bethan Perkins May 2014
# bethan.perkins@assimil.eu
########################################

Introduction:
This piece of code holds a record of the processing done to take differences between the ESA CCI SST datasets and the other datasets provided by the team.

Usage:
Import and run the modules. Each module takes differences between two differnt datasets.

Requirements:
- cdo installed (using "pip install cdo" on the command line)

==========================================================================
def sandbox():
    # Sandbox work. Delete this before final. Reproducing documentation steps.
    #re-grid the ESA SST L4 data
    cdo.remapbil("avhrr-only-v2.20070601.nc", input = "20070601120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_DM-v02.0-fv01.0.nc", output = "L4_DM_regrid_test.nc")

    #re-name the fields in the re-gridded ESA SST L4 data
    cdo.chname("analysed_sst,sst,sea_ice_fraction,ice,analysis_error,err", input = "L4_DM_regrid_test.nc", output = "L4_DM_regrid_rename_test.nc")

    #remove extraneous fields
    cdo.delname("anom", input="avhrr-only-v2.20070601.nc", output="avhrr-only-v2_remove.20070601.nc")
    cdo.delname("sea_ice_fraction_error,mask", input="L4_DM_regrid_rename_test.nc", output="L4_DM_regrid_rename_remove_test.nc")

    #convert degC into Kelvin
    cdo.addc("273.15", input = cdo.select("name=sst", input = "avhrr-only-v2_remove.20070601.nc"), output="avhrr-only-v2_remove_kelvin.20070601.nc")
    cdo.setunit("kelvin", input = cdo.select("name=sst", input = "avhrr-only-v2_remove_kelvin.20070601.nc"), output="avhrr-only-v2_remove_kelvin_complete.20070601.nc")

    # Take the differences
    cdo.sub(input = "L4_DM_regrid_rename_remove_test.nc"+" "+"avhrr-only-v2_remove_kelvin_complete.20070601.nc", output = "20070601_DM-avhrr-only.nc")
==========================================================================
"""

#setting up cdo tools
from cdo import *
cdo = Cdo()
import datetime

# Start with demo (DM) minus long term (LT) CCI SST datasets
reference_data_directory = "/media/Data_/ESA_CCI_SST/WORKSHOP_DATA/Gridded_data/CCI_LT_L4/"
variable_data_directory="/media/Data_/ESA_CCI_SST/WORKSHOP_DATA/Gridded_data/CCI_Demo_L4/"
output_data_directory="/media/Data_/ESA_CCI_SST/WORKSHOP_DATA/Gridded_data/CCI_Demo_L4-minus-CCI_LT_L4/"

# We're going to loop over days between 2007/06/01 and 2007/08/31
start = datetime.date(2007,6,1)
end = datetime.date(2007,8,1)
delta = end-start

for t in range(delta.days+1):

    #define the date that we're looking at in this step
    date = start + datetime.timedelta(days=t)

    #date as a string
    datestring = datetime.date.strftime(date,"%Y%m%d")

    #find the reference filename
    reference_file = glob.glob(reference_data_directory+datestring+"*.nc")

    #find the variable filename
    variable_file = glob.glob(variable_data_directory+datestring+"*.nc")

    #check there's only one file in each filename list
    if len(reference_file) is not 1:
        raise NameError("Two files match the date "+datestring+" in the folder "+reference_data_directory)

    if len(variable_file) is not 1:
        raise NameError("Two files match the date "+datestring+" in the folder "+variable_data_directory)

    #define output filename
    output_file = output_data_directory+datetime.date.strftime(date,"%Y%m%d")+"_CCI_Demo-minus-LT_L4.nc"

    # CDO COMMANDS
    # Take differences 
    cdo.sub(input = variable_file[0]+" "+reference_file[0], output = output_file)


