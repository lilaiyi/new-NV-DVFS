import pandas as pd
import numpy  as ny
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.svm import SVR
import joblib
from sklearn.preprocessing import StandardScaler
from models import xg_fitting, mean_absolute_percentage_error
colums = ['appName','coreF','time/ms','power','time/ms_2','SMACT','SMOCC','TENSO','DRAMA','FP64A'
           ,'FP32A','FP16A','SMACT_single_2','SMOCC_single_2','TENSO_single_2','DRAMA_single_2'
           ,'FP64A_single_2',
           'FP32A_single_2','FP16A_single_2','time/ms_single_1','time/ms_single_2','time_ratio'
           ,'time_ratio_2']
standardScaler = StandardScaler()




df = pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/test/merged_file_var_power_single_dcgm.csv')
df_test = pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/raw/task_3/merged_file_realapp.csv')


x=standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A",
        'SMACT_single_2','SMOCC_single_2','TENSO_single_2','FP64A_single_2',
        'DRAMA_single_2','FP32A_single_2','FP16A_single_2','power_single_1','power_single_2']])

y = df["power"]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,shuffle=False)
model_power = xg_fitting(x_train,y_train)

print("train power socre:")
train_y_pred = model_power.predict(x_train)
train_mae = mean_absolute_percentage_error(y_train, train_y_pred)
print(train_mae)


print("test power socre:")
test_y_pred = model_power.predict(x_test)
test_mae = mean_absolute_percentage_error(y_test, test_y_pred)
print(test_mae)

print("power score of ten ")
x_ten = standardScaler.fit_transform(df_test[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A",
        'SMACT_single_2','SMOCC_single_2','TENSO_single_2','FP64A_single_2',
        'DRAMA_single_2','FP32A_single_2','FP16A_single_2','power_single_1','power_single_2']])
y_ten = df_test["power"]
test_y_pred = model_power.predict(x_ten)
test_mae = mean_absolute_percentage_error(y_ten, test_y_pred)
print(test_mae)
