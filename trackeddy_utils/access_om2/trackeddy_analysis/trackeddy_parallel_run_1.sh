#!/bin/bash

#PBS -q hugemembw
#PBS -P x77
#PBS -l ncpus=140
##PBS -l ncpus=28
##PBS -l mem=1000Gb
#PBS -l mem=5000Gb
#PBS -l walltime=12:00:00
#PBS -l storage=gdata/v45+gdata/hh5+gdata/x77+scratch/x77+gdata/cj50
#PBS -N Eeddy_model
#PBS -l jobfs=100GB   

dataorigin='model'
ini=216
end=225
file_div=14

module load pbs
module load netcdf
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/access_om2/trackeddy_analysis/"

cd $cdir

./trackeddy_jobasignment.sh $ini $end 'run_model' $file_div
