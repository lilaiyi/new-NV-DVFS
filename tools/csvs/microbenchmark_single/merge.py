

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
import pandas as pd

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--benchmark-setting', type=str, help='gpu benchmark setting', default='v100-dvfs')
    parser.add_argument('--kernel-setting-1', type=str, help='kernels of benchmark', default='microbenchmark')
    parser.add_argument('--kernel-setting-2', type=str, help='kernels of benchmark', default='microbenchmark')
    parser.add_argument('--nvprof-enabled', action='store_true', help='enable nvprof functions')
    parser.add_argument('--dcgm-enabled', action='store_true', help='enable dcgm functions')
    parser.add_argument('--app-root', type=str, help='folder of applications', default='applications/linux')
    opt = parser.parse_args()

    
    # Read GPU application settings
    KS_SETTING_1 = '%s.cfg' % opt.kernel_setting_1
    cf_ks_1 = configparser.ConfigParser()
    cf_ks_1.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_1)
    benchmark_program_1 = cf_ks_1.sections()
 
    



    file_names = os.listdir()
    count = 0
    for i, app1 in enumerate(benchmark_program_1):
                args = json.loads(cf_ks_1.get(app1, 'args'))
                kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
                for argNo_1, arg_1 in enumerate(args):       
                        count += 1
                        app_name = app1+'-'+str(argNo_1)+'-'
                        target_df = pd.DataFrame()
                        merged_df = pd.DataFrame()
                        files = [file_name for file_name in file_names if app_name in file_name]
                        print(files)
                        dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
                        Performance_csv_file = [file_name for file_name in files if file_name.endswith("Performance.csv")]
                        Power_csv_file = [file_name for file_name in files if file_name.endswith("POWER.csv")]
                        df1 = pd.read_csv(dcgm_csv_file[0])
                        df2 = pd.read_csv(Performance_csv_file[0])
                        df3 = pd.read_csv(Power_csv_file[0])
                        # 合并三个DataFrame对象，相同head的行进行整合
                        target_df = df1.merge(df2, on=["appName", "coreF", "memF"], how="left")
                        target_df = target_df.merge(df3, on=["appName", "coreF", "memF"], how="left")
                        merged_df = pd.concat([merged_df, target_df], ignore_index=True)
                        if count == 1:
                            flag =True
                        else:
                            flag = False
                        merged_df.to_csv("merged_file.csv",  mode='a', header=flag,index=False)
    
    




