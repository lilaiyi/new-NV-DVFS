import pandas as pd
import numpy  as ny
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
import joblib
from sklearn.preprocessing import StandardScaler
import myscore
df = pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/V100-5:5/merged_file_ratio_dcgmOfdouble.csv')
df_test =pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/raw/double/merged_file_3.csv')

standardScaler = StandardScaler()

x= standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A"]])
y = df["power"]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
x_ten= standardScaler.fit_transform(df_test[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A"]])
y_ten = df_test["power"]
model_power = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
model_power.fit(x_train,y_train)
print("power socre:")
print(myscore.score(model_power.predict(x_test),y_test))
print("power score of ten")
print(myscore.score(model_power.predict(x_ten),y_ten))
joblib.dump(model_power, 'model_power.pkl')


x = standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A"]])
y = df[["time_ratio",'time_ratio_2']]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
x_ten= standardScaler.fit_transform(df_test[["coreF","SMACT","SMOCC","TENSO","DRAMA","FP64A","FP32A","FP16A"]])
y_ten = df_test[["time_ratio",'time_ratio_2']]
model_per = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
model_per.fit(x_train,y_train)
print("ratio socre:")
print(myscore.score(model_per.predict(x_test),y_test))
print("ratio score of ten")
print(myscore.score(model_per.predict(x_ten),y_ten))
joblib.dump(model_per, 'model_per.pkl')