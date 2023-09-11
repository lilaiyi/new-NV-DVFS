import time, argparse
import glob
import re
import configparser
import json
import csv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark-setting', type=str, help='gpu benchmark setting', default='v100-dvfs')
parser.add_argument('--kernel-setting', type=str, help='kernels of benchmark', default='synthetic')
parser.add_argument('--argno1', type=str, help='num of args', default='0')
parser.add_argument('--kernel-setting-2', type=str, help='kernels of benchmark', default='synthetic')
parser.add_argument('--argno2', type=str, help='num of args', default='0')
parser.add_argument('--percentage', type=str, help='no help', default='5:5')
parser.add_argument('--core-base', type=int, help='base core frequency', default=0)
parser.add_argument('--mem-base', type=int, help='base memory frequency', default=0)
opt = parser.parse_args()
gpucard = opt.benchmark_setting
version = opt.kernel_setting
version_2 = opt.kernel_setting_2
coreBase = opt.core_base
memBase = opt.mem_base
arg1=opt.argno1
arg2=opt.argno2
percentage  = opt.percentage
logRoot = '/home/lyli/NV-DVFS-Benchmark-master/logs/5:5/ALL/%s-%s-%s_%s-%s_percentage50:50' %( gpucard, version,arg1,version_2,arg2)

perf_filelist = glob.glob(r'%s/benchmark_%s_*perf.log' % (logRoot,version))
if version == version_2:
    temp=version_2+'2'
    perf_filelist2 = glob.glob(r'%s/benchmark_%s_*perf.log' % (logRoot,temp))
else:
    perf_filelist2 = glob.glob(r'%s/benchmark_%s_*perf.log' % (logRoot,version_2))
dcgm_filelist = glob.glob(r'%s/*dcgm.log' % (logRoot))

power_filelist = glob.glob(r'%s/*power.log' % (logRoot))

perf_filelist.sort()
perf_filelist2.sort()
dcgm_filelist.sort()
power_filelist.sort()

recs = []
recs2 = []
head = ["appName", "coreF", "memF", "argNo", "time/ms"]
for fp in perf_filelist:
    fn = fp.split('/')[-1]

    baseInfo = fn.split('_')
    appName = baseInfo[1]
    coreF = str(int(baseInfo[2][4:]) + coreBase)
    memF = str(int(baseInfo[3][3:]) + memBase)
    argNo = baseInfo[4]
    appName = appName + '-' + str(arg1)
    rec = [appName, coreF, memF, argNo]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'last \d+ iterats, average time is (\d+\.\d+) msec')
    timeRaw = filter(regex.search, content)
    timeRaw = list(timeRaw)
    remove_percentage = 0.4
    remove_count = int(len(timeRaw) * remove_percentage)
    timeRaw = timeRaw[remove_count:-remove_count]
    extracted_count = len(timeRaw)
    if len(timeRaw) == 0:
        continue
    time = 0
    for time_string in timeRaw:
        time += float(time_string.split()[-2].strip())
    average_time = time/extracted_count
    rec.append(average_time)
    recs.append(rec)
# prepare csv file
csvfile = open('csvs/test/%s-%s-%s-and-%s-%s-%s-%s-Performance.csv' % (gpucard, version,arg1,version_2,arg2,version,arg1), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])

rec=[]
for fp in perf_filelist2:
    fn = fp.split('/')[-1]

    baseInfo = fn.split('_')
    appName = baseInfo[1]
    coreF = str(int(baseInfo[2][4:]) + coreBase)
    memF = str(int(baseInfo[3][3:]) + memBase)
    argNo = baseInfo[4]
    appName = appName + '-' + str(arg2)
    rec = [appName, coreF, memF, argNo]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'last \d+ iterats, average time is (\d+\.\d+) msec')

    timeRaw = filter(regex.search, content)
    timeRaw = list(timeRaw)
    remove_percentage = 0.4
    remove_count = int(len(timeRaw) * remove_percentage)
    timeRaw = timeRaw[remove_count:-remove_count]
    extracted_count = len(timeRaw)
    if len(timeRaw) == 0:
        continue
    time = 0
    for time_string in timeRaw:
        time += float(time_string.split()[-2].strip())
    average_time = time/extracted_count
    rec.append(average_time)
    recs2.append(rec)
# prepare csv file
if version==version_2:
    csvfile = open('csvs/test/%s-%s-%s-and-%s-%s-%s-%s-Performance.csv' % (gpucard, version,arg1,version_2,arg2,temp,arg2), 'w')
else:   
    csvfile = open('csvs/test/%s-%s-%s-and-%s-%s-%s-%s-Performance.csv' % (gpucard, version,arg1,version_2,arg2,version_2,arg2), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs2:
    csvWriter.writerow(rec[:len(head)])



rec = []
recs = []
head = ["appName", "coreF", "memF", "power","var"]
for fp in power_filelist:
    fn = fp.split('/')[-1]
    appName = opt.kernel_setting+'-'+str(arg1)+'_'+opt.kernel_setting_2+'-'+str(arg2)
    baseInfo = fn.split('_')
    coreF = str(int(baseInfo[0][4:]) + coreBase)
    memF = str(int(baseInfo[1][3:]) + memBase)

    rec = [appName, coreF, memF]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'(\d+\.\d+) ms\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')

    PowerRaw = filter(regex.search, content)
    PowerRaw = list(PowerRaw)


    power_values = sorted([float(power_string.split()[-1].strip()) for power_string in PowerRaw], reverse=True)
    
    top_power_values = power_values[:10]
    average_power = sum(top_power_values) / len(top_power_values)
    sample_variance = sum((x - average_power) ** 2 for x in top_power_values) / (len(top_power_values) - 1)


    rec.append(average_power)
    rec.append(sample_variance)
    recs.append(rec)
# prepare csv file
csvfile = open('csvs/test/%s-%s-%s-and-%s-%s-POWER.csv' % (gpucard, version,arg1,version_2,arg2), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])




rec = []
recs = []
head = ["appName", "coreF", "memF","percentage",'SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']
for fp in dcgm_filelist:
    fn = fp.split('/')[-1]
    appName = opt.kernel_setting+'-'+str(arg1)+'_'+opt.kernel_setting_2+'-'+str(arg2)

    baseInfo = fn.split('_')
    coreF = str(int(baseInfo[0][4:]) + coreBase)
    memF = str(int(baseInfo[1][3:]) + memBase)

    rec = [appName, coreF, memF,percentage]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'GPU \d+\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)')
    
    dcgmRaw = filter(regex.search, content)
    dcgmRaw = list(dcgmRaw)
    remove_percentage = 0.4
    remove_count = int(len(dcgmRaw) * remove_percentage)
    dcgmRaw = dcgmRaw[remove_count:-remove_count]
    extracted_count = len(dcgmRaw)
    if len(dcgmRaw) == 0:
        continue
    SMACT = 0
    SMACT_C= 0
    SMOCC = 0
    SMOCC_C=0
    TENSO = 0
    TENSO_C=0 
    DRAMA = 0
    DRAMA_C=0
    FP64A = 0
    FP64A_C=0
    FP32A = 0
    FP32A_C=0
    FP16A = 0
    FP16A_C=0
    for dcgm_string in dcgmRaw:
        if(float(dcgm_string.split()[-1].strip())!=0):
            FP16A  += float(dcgm_string.split()[-1].strip())
            FP16A_C+=1
        if(float(dcgm_string.split()[-2].strip())!=0):    
            FP32A  += float(dcgm_string.split()[-2].strip())
            FP32A_C+=1
        if(float(dcgm_string.split()[-3].strip())!=0):    
            FP64A  += float(dcgm_string.split()[-3].strip())
            FP64A_C+=1
        if(float(dcgm_string.split()[-4].strip())!=0):    
            DRAMA  += float(dcgm_string.split()[-4].strip())
            DRAMA_C+=1
        if(float(dcgm_string.split()[-5].strip())!=0):    
            TENSO  += float(dcgm_string.split()[-5].strip())
            TENSO_C +=1
        if(float(dcgm_string.split()[-6].strip())!=0):    
            SMOCC  += float(dcgm_string.split()[-6].strip())
            SMOCC_C+=1
        if(float(dcgm_string.split()[-7].strip())!=0):    
            SMACT  += float(dcgm_string.split()[-7].strip())
            SMACT_C+=1
    average_SMACT=0
    average_SMOCC=0
    average_TENSO=0
    average_DRAMA=0
    average_FP64A=0
    average_FP32A=0
    average_FP16A=0
    if SMACT_C!=0:
        average_SMACT = SMACT/SMACT_C
    if SMOCC_C!=0:
        average_SMOCC = SMOCC/SMOCC_C
    if TENSO_C!=0:
        average_TENSO = TENSO/TENSO_C
    if DRAMA_C!=0:
        average_DRAMA = DRAMA/DRAMA_C
    if FP64A_C!=0:
        average_FP64A = FP64A/FP64A_C
    if FP32A_C!=0:
        average_FP32A = FP32A/FP32A_C
    if FP16A_C!=0:
        average_FP16A = FP16A/FP16A_C
    rec.append(average_SMACT)
    rec.append(average_SMOCC)
    rec.append(average_TENSO)
    rec.append(average_DRAMA)
    rec.append(average_FP64A)
    rec.append(average_FP32A)
    rec.append(average_FP16A)
    recs.append(rec)
# prepare csv file
csvfile = open('csvs/test/%s-%s-%s-and-%s-%s-dcgm.csv' % (gpucard, version,arg1,version_2,arg2), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])