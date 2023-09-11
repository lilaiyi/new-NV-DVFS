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
merged_df = pd.DataFrame()
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
                    target_df = pd.DataFrame()
                    complete_name = app1+'-'+str(argNo_1)+'_'+app2+'-'+str(argNo_2)
                    file_path = "merged_file.csv"
                    df = pd.read_csv(file_path)
                    data = df[df["appName"] == complete_name]
                    data_1380 = df[(df["coreF"] == 1380)&(df["appName"] == complete_name)]
                    time = data["time/ms"].values
                    freq_1380_time = data_1380["time/ms"].values[0]  
                    result_time = time / freq_1380_time
                    time_2 = data["time/ms_2"].values
                    freq_1380_time_2 = data_1380["time/ms_2"].values[0] 
                    result_time_2 = time_2 / freq_1380_time_2
                    # 将结果存储在新的列 "time_ratio" 中
                    data["time_ratio"] = result_time
                    data["time_ratio_2"] = result_time_2
                    merged_df = pd.concat([merged_df, data])   
        else:               
            args = json.loads(cf_ks_1.get(app1, 'args'))
            kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
            args_2 = json.loads(cf_ks_2.get(app2, 'args'))
            kernels_2 = json.loads(cf_ks_2.get(app2, 'kernels'))

            for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):
                    target_df = pd.DataFrame()
                    complete_name = app1+'-'+str(argNo_1)+'_'+app2+'-'+str(argNo_2)
                    file_path = "merged_file.csv"
                    df = pd.read_csv(file_path)
                    data = df[df["appName"] == complete_name]
                    data_1380 = df[(df["coreF"] == 1380)&(df["appName"] == complete_name)]
                    time = data["time/ms"].values
                    freq_1380_time = data_1380["time/ms"].values[0]  
                    result_time = time / freq_1380_time
                    time_2 = data["time/ms_2"].values
                    freq_1380_time_2 = data_1380["time/ms_2"].values[0] 
                    result_time_2 = time_2 / freq_1380_time_2
                    # 将结果存储在新的列 "time_ratio" 中
                    data["time_ratio"] = result_time
                    data["time_ratio_2"] = result_time_2
                    merged_df = pd.concat([merged_df, data])   
merged_df.to_csv("merged_file_ratio.csv", index=False)
