#!/bin/bash

#if [ "$dataorigin" == "model" ];
#then
#  ncp=$(($end-$ini))
#else
#  ncp=$((($end-$ini)*4))
#fi

#PBS -q express
#PBS -P x77
#PBS -l ncpus=16
#PBS -l mem=100Gb
#PBS -l walltime=24:00:00
#PBS -N chelt2teddy

file_div=16

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/chelton2py/"

cd $cdir 

./jobasignment.sh $file_div 'run'
