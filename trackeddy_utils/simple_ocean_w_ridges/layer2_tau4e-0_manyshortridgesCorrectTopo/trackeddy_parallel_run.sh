#!/bin/bash
#PBS -q normalbw
#PBS -P x77
#PBS -l ncpus=28
#PBS -l mem=100Gb
#PBS -l walltime=48:00:00
#PBS -N 2L_TEddy

ini=22
end=49

module load pbs
module load netcdf/4.3.3.1
module use /projects/v45/modules
module load cmstools
module use /g/data3/hh5/public/modules
module load conda/analysis3

expt='layer2_tau4e-0_manyshortridgesCorrectTopo'

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/simple_ocean_w_ridges/$expt/"

cd $cdir

./trackeddy_jobasignment.sh $ini $end 'run'
