#!/bin/bash

#PBS -q normal
#PBS -P x77
#PBS -l ncpus=1488
#PBS -l mem=3000Gb
#PBS -l walltime=1:00:00
#PBS -N pd_eddy
#PBS -l storage=gdata/v45+gdata/hh5+gdata/x77+scratch/x77+gdata/cj50
#PBS -l jobfs=100GB

dataorigin='model'
ini=628
end=731
file_div=14

module load pbs
module load netcdf
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/access_om2_3rd_cycle/pandas_fields/"

cd $cdir

./trackeddy_jobasignment.sh $ini $end 'run_model' $file_div
