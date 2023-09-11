import os
import pandas as pd
import json
import configparser


KS_SETTING_1 = 'microbenchmark.cfg' 
KS_SETTING_2 = 'microbenchmark.cfg' 
cf_ks_1 = configparser.ConfigParser()
cf_ks_1.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_1)
benchmark_program_1 = cf_ks_1.sections()
cf_ks_2 = configparser.ConfigParser()
cf_ks_2.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_2)
benchmark_program_2 = cf_ks_2.sections()
file_names = os.listdir()
count = 0
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
                    count +=1
                    merged_df = pd.DataFrame()    
                    target_df = pd.DataFrame()
                    appname1 = app1+'-'+str(argNo_1)
                    appname2 = app2+'-'+str(argNo_2)
                    Pname = app2+'2'+'-'+str(argNo_2)
                    complete_name = appname1+'-and-'+appname2+'-'
                    files = [file_name for file_name in file_names if complete_name in file_name]
                    dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
                    Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname1)]
                    Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%Pname)]
                    Power_csv_file = [file_name for file_name in files if file_name.endswith("%sPOWER.csv"%(complete_name))]
                    df1 = pd.read_csv(dcgm_csv_file[0])
                    df2 = pd.read_csv(Performance_csv_file_app1[0])
                    df4 = pd.read_csv(Performance_csv_file_app2[0])
                    df3 = pd.read_csv(Power_csv_file[0])
                    # 合并三个DataFrame对象，相同head的行进行整合
                    target_df = df1.merge(df2[[ "coreF", "memF", "time/ms"]], on=[ "coreF", "memF"], how="left")
                    target_df = target_df.merge(df3[[ "coreF", "memF", "power","var"]], on=["coreF", "memF"], how="left")
                    target_df = target_df.merge(df4[[ "coreF", "memF", "time/ms"]], on=[ "coreF", "memF"], how="left", suffixes=('', '_2'))

                    merged_df = pd.concat([merged_df, target_df], ignore_index=True)
                    if count == 1:
                        flag =True
                    else:
                        flag = False
                    merged_df.to_csv("merged_file.csv",  mode='a', header=flag,index=False)
        else:               
            args = json.loads(cf_ks_1.get(app1, 'args'))
            kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
            args_2 = json.loads(cf_ks_2.get(app2, 'args'))
            kernels_2 = json.loads(cf_ks_2.get(app2, 'kernels'))

            for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):
                    count+=1
                    merged_df = pd.DataFrame()    
                    target_df = pd.DataFrame()
                    appname1 = app1+'-'+str(argNo_1)
                    appname2 = app2+'-'+str(argNo_2)
                    complete_name = appname1+'-and-'+appname2+'-'
                    files = [file_name for file_name in file_names if complete_name in file_name]
                    dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
                    Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname1)]
                    Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname1)]
                    Power_csv_file = [file_name for file_name in files if file_name.endswith("%sPOWER.csv"%(complete_name))]
                    df1 = pd.read_csv(dcgm_csv_file[0])
                    df2 = pd.read_csv(Performance_csv_file_app1[0])
                    df4 = pd.read_csv(Performance_csv_file_app2[0])
                    df3 = pd.read_csv(Power_csv_file[0])
                    # 合并三个DataFrame对象，相同head的行进行整合
                    target_df = df1.merge(df2[[ "coreF", "memF", "time/ms"]], on=[ "coreF", "memF"], how="left")
                    target_df = target_df.merge(df3[[ "coreF", "memF", "power","var"]], on=[ "coreF", "memF", ], how="left")
                    target_df = target_df.merge(df4[[ "coreF", "memF", "time/ms"]], on=[ "coreF", "memF", ], how="left", suffixes=('', '_2'))

                    merged_df = pd.concat([merged_df, target_df], ignore_index=True)
                    if count == 1:
                        flag =True
                    else:
                        flag = False
                    merged_df.to_csv("merged_file.csv",  mode='a', header=flag,index=False)
