import pandas as pd
import numpy  as ny
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.svm import SVR
import joblib
from sklearn.preprocessing import StandardScaler
import myscore
colums = ['appName','coreF','time/ms','power','time/ms_2','SMACT','SMOCC','TENSO','DRAMA','FP64A'
           ,'FP32A','FP16A','SMACT_single_2','SMOCC_single_2','TENSO_single_2','DRAMA_single_2'
           ,'FP64A_single_2',
           'FP32A_single_2','FP16A_single_2','time/ms_single_1','time/ms_single_2','time_ratio'
           ,'time_ratio_2']
standardScaler = StandardScaler()




df = pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/V100-5:5/merged_file_5.csv')
df_test = pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/raw/task_3/merged_file_3.csv')


x=standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A",
        'SMACT_single_2','SMOCC_single_2','TENSO_single_2','FP64A_single_2',
        'DRAMA_single_2','FP32A_single_2','FP16A_single_2']])

y = df["power"]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,shuffle=False)
model_power = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
model_power.fit(x_train,y_train)
print("power socre:")
print(myscore.score(model_power.predict(x_test),y_test))
joblib.dump(model_power, 'model_power.pkl')
print("power score of ten ")
x_ten = standardScaler.fit_transform(df_test[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A",
        'SMACT_single_2','SMOCC_single_2','TENSO_single_2','FP64A_single_2',
        'DRAMA_single_2','FP32A_single_2','FP16A_single_2']])
y_ten = df_test["power"]
print(myscore.score(model_power.predict(x_ten),y_ten))


x=standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A",
        'SMACT_single_2','SMOCC_single_2','TENSO_single_2','FP64A_single_2',
        'DRAMA_single_2','FP32A_single_2','FP16A_single_2']])


y = df[["time_ratio",'time_ratio_2']]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,shuffle=False)
model_per = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
model_per.fit(x_train,y_train)
print("ratio socre:")
print(myscore.score(model_per.predict(x_test),y_test))

print("per score of ten ")
x_ten = standardScaler.fit_transform(df_test[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A",
        'SMACT_single_2','SMOCC_single_2','TENSO_single_2','FP64A_single_2',
        'DRAMA_single_2','FP32A_single_2','FP16A_single_2']])
y_ten = df_test[["time_ratio",'time_ratio_2']]
print(myscore.score(model_per.predict(x_ten),y_ten))
joblib.dump(model_per, 'model_per.pkl')