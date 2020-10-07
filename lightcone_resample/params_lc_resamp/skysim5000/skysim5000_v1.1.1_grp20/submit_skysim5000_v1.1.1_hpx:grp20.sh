#!/bin/bash
qsub -n 1 -t 720 -A LastJourney -o /gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/0_1_grp20.out -e /gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/0_1_grp20.err  --debuglog=/gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/0_1_grp20.cobalt  /soft/libraries/anaconda-unstable/bin/python ./lc_resample.py params_lc_resamp/skysim5000/skysim5000_v1.1.1_grp20/skysim5000_v1.1.1_z_0_1_hpx:grp20.param
qsub -n 1 -t 720 -A LastJourney -o /gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/1_2_grp20.out -e /gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/1_2_grp20.err  --debuglog=/gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/1_2_grp20.cobalt  /soft/libraries/anaconda-unstable/bin/python ./lc_resample.py params_lc_resamp/skysim5000/skysim5000_v1.1.1_grp20/skysim5000_v1.1.1_z_1_2_hpx:grp20.param
qsub -n 1 -t 720 -A LastJourney -o /gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/2_3_grp20.out -e /gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/2_3_grp20.err  --debuglog=/gpfs/mira-fs0/projects/DarkUniverse_esp/kovacs/OR_5000/skysim5000_v1.1.1/logs/2_3_grp20.cobalt  /soft/libraries/anaconda-unstable/bin/python ./lc_resample.py params_lc_resamp/skysim5000/skysim5000_v1.1.1_grp20/skysim5000_v1.1.1_z_2_3_hpx:grp20.param
