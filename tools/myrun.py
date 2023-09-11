import json
import configparser
import os

KS_SETTING_1 = 'microbenchmark.cfg' 
KS_SETTING_2 = 'microbenchmark.cfg' 
cf_ks_1 = configparser.ConfigParser()
cf_ks_1.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_1)
benchmark_program_1 = cf_ks_1.sections()
cf_ks_2 = configparser.ConfigParser()
cf_ks_2.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_2)
benchmark_program_2 = cf_ks_2.sections()
for i, app1 in enumerate(benchmark_program_1):
    for j, app2 in enumerate(benchmark_program_2):
        if j < i:
            continue
        if j==i: 
            args = json.loads(cf_ks_1.get(app1, 'args'))
            kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
            args_2 = json.loads(cf_ks_2.get(app2, 'args'))
            kernels_2 = json.loads(cf_ks_2.get(app2, 'kernels'))


            for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):

                    if argNo_2<argNo_1 :
                        continue
                    cmd="python ExtracterFormicrobenchmark.py   --kernel-setting %s --kernel-setting-2 %s --argno1 %s --argno2 %s"%(app1,app2,argNo_1,argNo_2)
                    os.system(cmd)
        else:               
            args = json.loads(cf_ks_1.get(app1, 'args'))
            kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
            args_2 = json.loads(cf_ks_2.get(app2, 'args'))
            kernels_2 = json.loads(cf_ks_2.get(app2, 'kernels'))

            for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):
                    cmd="python ExtracterFormicrobenchmark.py   --kernel-setting %s --kernel-setting-2 %s --argno1 %s --argno2 %s"%(app1,app2,argNo_1,argNo_2)
                    os.system(cmd)