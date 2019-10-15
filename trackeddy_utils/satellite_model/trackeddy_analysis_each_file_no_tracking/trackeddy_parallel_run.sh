#!/bin/bash

#PBS -q normalbw
#PBS -P v45
#PBS -l ncpus=308
# #PBS -l ncpus=12
#PBS -l mem=2750Gb
# #PBS -l mem=200Gb
#PBS -N Eeddy_sat
# #PBS -l walltime=48:00:00
#PBS -l walltime=24:00:00

dataorigin='satellite'
ini=1993
end=2017

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/satellite_model/trackeddy_analysis_each_file_no_tracking/"

cd $cdir

./trackeddy_jobasignment.sh $dataorigin $ini $end 'run_satel'
