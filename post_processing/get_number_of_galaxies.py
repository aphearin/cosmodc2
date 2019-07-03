import glob
import re
import numpy as np
import h5py
import os
import re

image_list = [8786, 8787, 8788, 8789, 8790, 8791, 8792, 8793, 8794, 8913, 8914, 8915, 8916, 8917, 8918, 8919, 8920, 8921, 9042, 9043, 9044, 9045, 9046, 9047, 9048, 9049,
                 9050, 9169, 9170, 9171, 9172, 9173, 9174, 9175, 9176, 9177, 9178, 9298, 9299, 9300, 9301, 9302, 9303, 9304, 9305, 9306, 9425, 9426, 9427, 9428, 9429, 9430,
                 9431, 9432, 9433, 9434, 9554, 9555, 9556, 9557, 9558, 9559, 9560, 9561, 9562, 9681, 9682, 9683, 9684, 9685, 9686, 9687, 9688, 9689, 9690, 9810, 9811, 9812,
                 9813, 9814, 9815, 9816, 9817, 9818, 9937, 9938, 9939, 9940, 9941, 9942, 9943, 9944, 9945, 9946, 10066, 10067, 10068, 10069, 10070, 10071, 10072, 10073, 10074, 10193,
                 10194, 10195, 10196, 10197, 10198, 10199, 10200, 10201, 10202, 10321, 10322, 10323, 10324, 10325, 10326, 10327, 10328, 10329, 10444, 10445, 10446, 10447, 10448, 10449, 10450,
                 10451, 10452]


master_dir='/global/projecta/projectdirs/lsst/groups/CS/cosmoDC2/'
#filedir = 'cosmoDC2_v1.0.0_full_highres'
#version = '1.0.0'

def write_num_gal(filedir, version, image='image'):
    filedir = os.path.join(master_dir, filedir)
    filelist = sorted(glob.glob(filedir+'/*.hdf5'))

    outfile = 'cosmoDC2_check_num_gal_{}.txt'.format(image)
    print('Opening {}'.format(outfile))
    with open(outfile, 'w') as fh:
        fh.write("'{}' :\n".format(version))
        num_gals={}

        #test = [f for f in filelist if '9556' in f]
        for f in filelist:
        #for f in test:
            fname = os.path.basename(f)
            h5 = h5py.File(f, 'r')
            num = len(h5['galaxyProperties']['galaxyID'])
            healpix = re.findall(r'\d+', re.split('healpix', f)[-1])[0]
            #print('{}: {}, num= {}'.format(f, healpix, num))
            if healpix in num_gals.keys():
                num_gals[healpix] += num
            else:
                num_gals[healpix] = num

        #print(num_gals)
        for k in sorted(num_gals.keys()):
            if len(image) > 0 and int(k) not in image_list:
                continue
            fh.write('{} : {}\n'.format(k, num_gals[k]))

        fh.close

    return
