import os
import sys
import argparse
import subprocess
import time
import re
import configparser
import json
import threading
import subprocess


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--benchmark-setting', type=str, help='gpu benchmark setting', default='v100-dvfs')
    parser.add_argument('--kernel-setting-1', type=str, help='kernels of benchmark', default='microbenchmark')
    parser.add_argument('--kernel-setting-2', type=str, help='kernels of benchmark', default='microbenchmark')
    parser.add_argument('--nvprof-enabled', action='store_true', help='enable nvprof functions')
    parser.add_argument('--dcgm-enabled', action='store_true', help='enable dcgm functions')
    parser.add_argument('--app-root', type=str, help='folder of applications', default='applications/linux')
    opt = parser.parse_args()
    print(opt)
    
    application_dir = opt.app_root

    
    # Read GPU application settings
    KS_SETTING_1 = '%s.cfg' % opt.kernel_setting_1
    KS_SETTING_2 = '%s.cfg' % opt.kernel_setting_2
    cf_ks_1 = configparser.ConfigParser()
    cf_ks_1.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_1)
    benchmark_program_1 = cf_ks_1.sections()
    cf_ks_2 = configparser.ConfigParser()
    cf_ks_2.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_2)
    benchmark_program_2 = cf_ks_2.sections()
    





    for i, app1 in enumerate(benchmark_program_1):
                args = json.loads(cf_ks_1.get(app1, 'args'))
                kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
                for argNo_1, arg_1 in enumerate(args):       
                       os.system('python SinglePerExtracter.py --kernel-setting %s --argnum %s'%(app1,str(argNo_1)))


