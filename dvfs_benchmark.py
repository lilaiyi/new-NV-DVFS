import os
import sys
import argparse
import subprocess
import time
import re
import configparser
import json
from utils.profiler import PowerProfiler 
from utils.profiler import NvProfiler
from utils.profiler import DCGMProfiler
from utils.dvfs_control import DVFSController
import threading
import subprocess

option_count = []
class Benchmark:

    # TODO: write the benchmark arguments as one line into the log.
    def __init__(self, app_dir, log_dir, application, arg_no, arg, kernel, core_freq, mem_freq, device_id=0, percentage='50',tag=False):

        # app_exec_cmd = './%s/%s %s -device=%d -secs=%d >> %s/%s' % (
        self.base_cmd = './%s/%s %s' % (
            app_dir,
            application,
            arg
        )

        # arg, number = re.subn('-device=[0-9]*', '-device=%d' % cuda_dev_id, arg)
        
        self.powerlog = './%s/core%d_mem%d_input%03d_power.log' % (log_dir, core_freq, mem_freq, arg_no)
        if tag == True:
            name = application+'2'
            self.perflog = './%s/benchmark_%s_core%d_mem%d_input%03d_perf.log' % (log_dir, name, core_freq, mem_freq, arg_no)
        else :
            self.perflog = './%s/benchmark_%s_core%d_mem%d_input%03d_perf.log' % (log_dir, application, core_freq, mem_freq, arg_no)    
        self.metricslog = './%s/benchmark_%s_core%d_mem%d_input%03d_metrics.log' % (log_dir, application, core_freq, mem_freq, arg_no)
        self.dcgmlog = './%s/benchmark_%s_core%d_mem%d_input%03d_dcgm.log' % (log_dir, application, core_freq, mem_freq, arg_no)
        self.percentage = percentage
        # write the argument info into the log.
        os.system('echo "kernel name:" >> %s' % self.perflog)
        os.system('echo "%s" >> %s' % (kernel, self.perflog))

    def get_power_file(self):

        return self.powerlog

    def get_performance_file(self):

        return self.perflog

    def get_metrics_file(self):

        return self.metricslog

    def get_dcgm_file(self):

        return self.dcgmlog

    def get_run_command(self, device_id=0, iters=100, secs=None):

        if secs is None:
            command = '%s -device=%d -iters=%d' % (self.base_cmd, device_id, iters)
        else:
            command = '%s -device=%d -secs=%d' % (self.base_cmd, device_id, secs)
        return command

    def run(self, device_id=0, iters=10000, secs=20):
        command = self.get_run_command(device_id, iters=iters, secs=secs)
        command += ' 1>>%s 2>&1' % self.perflog
        print(command)
        os.system(command)
    
    def get_subprocess_command(self, device_id=0, iters=10000, secs=20):
        set_percentage = 'export CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=%s'%self.percentage
        command = self.get_run_command(device_id, iters=iters, secs=secs)
        command += ' 1>>%s 2>&1' % self.perflog
        combined_command = '%s;%s'%(set_percentage,command)
        return combined_command


def get_config(bench_file, nvprof_enabled=True, dcgm_enabled=True):

    BS_SETTING = '%s.cfg' % bench_file

    bench_args = {}
    
    # Reading benchmark settings
    cf_bs = configparser.ConfigParser()
    cf_bs.read("configs/benchmarks/%s" % BS_SETTING)

    # device info
    bench_args['cuda_dev_id'] = cf_bs.getint("device", "cuda_device_id")
    bench_args['nvins_dev_id'] = cf_bs.getint("device", "nvins_device_id")
    bench_args['nvsmi_dev_id'] = cf_bs.getint("device", "nvsmi_device_id")

    # global running config
    bench_args['running_time'] = cf_bs.getint("global", "secs")
    bench_args['rest_time'] = cf_bs.getint("global", "rest_time")
    bench_args['pw_sample_int'] = cf_bs.getint("global", "power_sample_interval")

    # dvfs control
    bench_args['core_freqs'] = json.loads(cf_bs.get("dvfs_control", "coreF"))
    bench_args['mem_freqs'] = json.loads(cf_bs.get("dvfs_control", "memF"))
    bench_args['freqs'] = [(coreF, memF) for coreF in bench_args['core_freqs'] for memF in bench_args['mem_freqs']]

    # nvprof
    if not nvprof_enabled:
        bench_args['nvprof'] = None
    else:
        bench_args['nvprof'] = {}
        bench_args['nvprof']['time_command']= cf_bs.get("nvprof", "time_command")
        bench_args['nvprof']['thread_cmd'] = cf_bs.get("nvprof", "setting_command")
        bench_args['nvprof']['metrics_cmd'] = cf_bs.get("nvprof", "metrics_command")
        bench_args['nvprof']['metrics_list'] = json.loads(cf_bs.get("nvprof", "metrics"))

    # dcgm
    if not dcgm_enabled:
        bench_args['dcgm'] = None
    else:
        bench_args['dcgm'] = {}
        bench_args['dcgm']['metrics_list'] = json.loads(cf_bs.get("dcgm", "metrics"))

    return bench_args


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

    
    bench_args = get_config(opt.benchmark_setting, opt.nvprof_enabled, opt.dcgm_enabled)
    
    # Read GPU application settings
    KS_SETTING_1 = '%s.cfg' % opt.kernel_setting_1
    KS_SETTING_2 = '%s.cfg' % opt.kernel_setting_2
    cf_ks_1 = configparser.ConfigParser()
    cf_ks_1.read("configs/kernels/%s" % KS_SETTING_1)
    benchmark_program_1 = cf_ks_1.sections()
    cf_ks_2 = configparser.ConfigParser()
    cf_ks_2.read("configs/kernels/%s" % KS_SETTING_2)
    benchmark_program_2 = cf_ks_2.sections()
    
    power_profiler = PowerProfiler(
        device_id = bench_args['nvsmi_dev_id'],
        sample_interval = bench_args['pw_sample_int']
    )

    dvfs_controller = DVFSController(device_id=bench_args['nvsmi_dev_id'])
    dvfs_controller.activate()

    if bench_args['nvprof'] is not None:
        nvprofiler = NvProfiler(
            device_id=bench_args['cuda_dev_id'],
            metrics=bench_args['nvprof']['metrics_list']
        )
    if bench_args['dcgm'] is not None:
        dcgm_profiler = DCGMProfiler(
            device_id = bench_args['nvsmi_dev_id'],
            sample_interval = bench_args['pw_sample_int'],
            metrics=bench_args['dcgm']['metrics_list']
        )

    print(bench_args['freqs'])
    count  = 0

    core_freq = 1380 
    mem_freq = 877        
    # set specific frequency
    dvfs_controller.set_frequency(core_freq, mem_freq)
    for i, app1 in enumerate(benchmark_program_1):
                args = json.loads(cf_ks_1.get(app1, 'args'))
                kernels = json.loads(cf_ks_1.get(app1, 'kernels'))
                for argNo_1, arg_1 in enumerate(args):       
                        logging_dir =  'logs/microbenchmark/%s-%s-%d' % (opt.benchmark_setting, app1, argNo_1)
                        try:
                            os.makedirs(logging_dir)
                        except OSError:
                            pass
                        kernel_1 = kernels[argNo_1]
                        bench_1 = Benchmark(
                            app_dir = application_dir,
                            log_dir = logging_dir,
                            application = app1,
                            arg_no = argNo_1,
                            arg = arg_1,
                            kernel = kernel_1,
                            core_freq = core_freq,
                            mem_freq = mem_freq
                        )
                        powerlog = './%s/core%d_mem%d_power.log' % (logging_dir, int(core_freq), int(mem_freq))
                        dcgmlog = './%s/core%d_mem%d_dcgm.log' % (logging_dir, int(core_freq), int(mem_freq))
                        # start record power data
                        power_profiler.start(powerlog)
                        time.sleep(bench_args['rest_time'])
            
                        # start dcgm
                        if bench_args['dcgm'] is not None:
                            dcgm_profiler.start(dcgmlog)
                            time.sleep(bench_args['rest_time'])
            
                        # execute program to collect power (and dcgm optionally) data
                        # os.system('export CUDA_VISIBLE_DEVICES=%s'%bench_args['cuda_dev_id'])
                        # os.system('export CUDA_MPS_ENABLE_PER_CTX_DEVICE_MULTIPROCESSOR_PARTITIONING=1')
                        bench_1.run(secs=10)
                        # def run_bench_1():
                        #     bench_1.run(device_id=bench_args['cuda_dev_id'])
                        # thread = threading.Thread(target=run_bench_1)
                        # thread.start()
                        # thread.join()
                        # bench_2.run(device_id=bench_args['cuda_dev_id'])
                        
                        time.sleep(bench_args['rest_time'])
                        
            
                        # stop record power (and dcgm optionally) data
                        power_profiler.end()
                        if bench_args['dcgm'] is not None:
                            dcgm_profiler.end()

                        if bench_args['nvprof'] is not None:
                            # use nvprof to collect the execution time
                            nvprofiler.collect_time(bench_1)
                            time.sleep(bench_args['rest_time'])
                            
                            # use nvprof to collect the thread setting
                            nvprofiler.collect_thread_setting(bench_1)
                            time.sleep(bench_args['rest_time'])
                            
                            # use nvprof to collect the metrics
                            nvprofiler.collect_metrics(bench_1)
                            time.sleep(bench_args['rest_time'])
            
    dvfs_controller.reset()
