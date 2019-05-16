#!/bin/bash

#PBS -q expressbw
#PBS -P v45
#PBS -l ncpus=28
#PBS -l mem=250Gb
#PBS -l walltime=24:00:00
#PBS -N Reddy_M

ini=127
end=154

module use /g/data3/hh5/public/modules
module load conda/analysis3

cdir="/home/156/jm5970/github/phd_source/trackeddy_utils/simple_ocean_w_ridges/reconstruct_fields/"

cd $cdir

./trackeddy_jobasignment.sh $ini $end 'run_model'
