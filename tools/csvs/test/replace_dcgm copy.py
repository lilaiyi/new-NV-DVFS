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
merged_df = pd.DataFrame()
file_path = "merged_file_with_single_dcgm.csv"
df = pd.read_csv(file_path)
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
                    complete_name = app1+'-'+str(argNo_1)+'_'+app2+'-'+str(argNo_2)
                    data = df[df["appName"] == complete_name]
                    data_1380 = data[(data["coreF"] == 1380)]
                    columns_to_replace = ["SMACT", "SMOCC", "TENSO", "DRAMA", "FP64A", "FP32A", "FP16A",
                                            "SMACT_single_2","SMOCC_single_2","TENSO_single_2","DRAMA_single_2",
                                            "power_single_1","power_single_2",
                                            "FP64A_single_2","FP32A_single_2","FP16A_single_2",
                                            "time/ms_single_1","time/ms_single_2"]

                    for column in columns_to_replace:
                        # 获取coreF不为1380的行的索引
                        indices_to_replace = data.index[ (data["coreF"] != 1380)]
                        
                        # 使用coreF为1380的行的数据进行替换
                        data.loc[indices_to_replace, column] = data_1380[column].values[0]
                    
                    # 将修改后的数据存储在merged_df中
                    merged_df = pd.concat([merged_df, data])
        else:               
            args = json.loads(cf_ks_1.get(app1, 'args'))
            kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
            args_2 = json.loads(cf_ks_2.get(app2, 'args'))
            kernels_2 = json.loads(cf_ks_2.get(app2, 'kernels'))

            for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):
                    complete_name = app1+'-'+str(argNo_1)+'_'+app2+'-'+str(argNo_2)
                    data = df[df["appName"] == complete_name]
                    data_1380 = data[(data["coreF"] == 1380)]
                    columns_to_replace = ["SMACT", "SMOCC", "TENSO", "DRAMA", "FP64A", "FP32A", "FP16A",
                                            "SMACT_single_2","SMOCC_single_2","TENSO_single_2","DRAMA_single_2",
                                            "power_single_1","power_single_2",
                                            "FP64A_single_2","FP32A_single_2","FP16A_single_2",
                                            "time/ms_single_1","time/ms_single_2"]
                    for column in columns_to_replace:
                        # 获取coreF不为1380的行的索引
                        indices_to_replace = data.index[ (data["coreF"] != 1380)]
                        
                        # 使用coreF为1380的行的数据进行替换
                        data.loc[indices_to_replace, column] = data_1380[column].values[0]
                    
                    # 将修改后的数据存储在merged_df中
                    merged_df = pd.concat([merged_df, data])



merged_df.to_csv("merged_file_after_replace.csv", index=False)