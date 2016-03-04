#!/usr/bin/env python
'''
Service to monitor one or more vmx path[s] and restart the vmx[s] if necessary

Requirements:
    VMware Fusion 7.x Professional
    OS X 10.9.5+ (compatible with 10.10)

usage: vfused.py [-h] [--list] [--monitor] [--add ADD] [--remove REMOVE]
                [--reset RESET] [--get-ip GET_IP]

optional arguments:
  -h, --help       show this help message and exit
  --list           List monitored and running VMs
  --monitor        Service to monitor VMs
  --add ADD        Add monitoring for /path/to/vmx
  --remove REMOVE  Remove monitoring for /path/to/vmx
  --reset RESET    Reset /path/to/vmx
  --get-ip GET_IP  Get IP for /path/to/vmx
'''
##############################################################################
# Copyright 2016 Joseph Chilcote
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

__author__  = 'Joseph Chilcote (chilcote@gmail.com)'
__version__ = '1.0.0'

import os, sys, subprocess
import plistlib
import argparse
import time
import shutil
import syslog
from random import randint

class VMXMonitor(object):
    '''Monitoring a vmx file'''

    def __init__(self, 
                plist = os.path.expanduser('~/Library/Preferences/com.chilcote.vfused.plist'),
                vmrun = '/Applications/VMware Fusion.app/Contents/Library/vmrun'):
        self.plist = plist
        if not os.path.exists(self.plist):
            plistlib.writePlist({}, plist)
        self.d = plistlib.readPlist(plist)
        self.vmrun = vmrun

    def set_start(self, vmx, job_id=None):
        if not self.d or not vmx in self.d.values()[0]:
            if not job_id:
                job_id = randint(1000, 9999)
            self.d[str(job_id)] = [str(vmx), 'start', '', '']
            plistlib.writePlist(self.d, self.plist)

    def set_stop(self, vmx, job_id=None):
        for k, v in self.d.items():
            if v[0] == vmx:
                self.d[k][1] = 'stop'
        plistlib.writePlist(self.d, self.plist)

    def set_reset(self, vmx, job_id=None):
        for k, v in self.d.items():
            if v[0] == vmx:
                self.d[k][1] = 'reset'
        plistlib.writePlist(self.d, self.plist)

    def remove(self, vmx):
        for k, v in self.d.items():
            if v[0] == vmx:
                del self.d[k]
        plistlib.writePlist(self.d, self.plist)

    def set_running(self, vmx):
        for k, v in self.d.items():
            if v[0] == vmx:
                self.d[k][1] = 'running'
                self.d[k][2] = self.get_ip(vmx)
                self.d[k][3] = str(self.get_pid(vmx))
        plistlib.writePlist(self.d, self.plist)

    def get_pid(self, vmx):
        for root, dirs, files in os.walk('/var/run/vmware'):
            for i in files:
                full_path = root + '/' + i
                if os.path.realpath(full_path) in vmx:
                    return os.path.dirname(full_path).split('_')[-1]

    def get_monitored(self):
        l = []
        for i in self.d.values():
            l.append(i[0])
        return l

    def is_running(self, vmx):
        for root, dirs, files in os.walk('/var/run/vmware'):
            for i in files:
                full_path = root + '/' + i
                if os.path.realpath(full_path) in vmx:
                    return True

    def is_scheduled(self, vmx):
        for k, v in self.d.items():
            if v[0] == vmx:
                if v[1] == 'start' or v[1] == 'running':
                    return True

    def to_be_removed(self, vmx):
        for k, v in self.d.items():
            if v[0] == vmx:
                if v[1] == 'stop':
                    return True

    def to_be_reset(self, vmx):
        for k, v in self.d.items():
            if v[0] == vmx:
                if v[1] == 'reset':
                    return True

    def get_scheduled(self):
        d = {}
        for k, v in self.d.items():
            if v[1] == 'start' or v[1] == 'running':
                d[k] = v
        return d

    def get_running(self):
        d = {}
        cmd = [self.vmrun, 'list']
        output = subprocess.check_output(cmd)
        for line in output.splitlines():
            if 'Total running VMs' in line:
                if int(line.split(': ')[1]) == 0:
                    return d
            else:
                d[line.strip()] = self.get_pid(line.strip())
        return d

    def start_vmx(self, vmx):
        cmd = [self.vmrun, 'start', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            syslog.syslog(syslog.LOG_ALERT, 'Could not process:\t%s' % vmx)

    def stop_vmx(self, vmx):
        cmd = [self.vmrun, 'stop', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            syslog.syslog(syslog.LOG_ALERT, 'Could not process:\t%s' % vmx)

    def reset_vmx(self, vmx):
        cmd = [self.vmrun, 'reset', vmx]
        task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = task.communicate()
        if err:
            syslog.syslog(syslog.LOG_ALERT, 'Could not process:\t%s' % vmx)

    def delete_vm(self, vmx):
        if os.path.exists(os.path.dirname(vmx)):
            shutil.rmtree(os.path.dirname(vmx))

    def job_to_vmx(self, job_id):
        for k, v in self.d.items():
            if job_id == k:
                return v[0]

    def get_ip(self, vmx):
        count = 1
        while count <= 36:
            cmd = [self.vmrun, 'getGuestIPAddress', vmx]
            task = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, err = task.communicate()
            if not task.returncode == 255:
                break
            count += 1
            time.sleep(5)
        if 'Error' in out:
            return ''
        return out.strip()

    def vmx_is_valid(self, vmx):
        if os.path.splitext(vmx)[-1] == '.vmx':
            if os.path.exists(vmx):
                return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', help='List monitored and running VMs',
                        action='store_true')
    parser.add_argument('--monitor', help='Service to monitor VMs', action='store_true')    
    parser.add_argument('--add', help='Add monitoring for /path/to/vmx')
    parser.add_argument('--remove', help='Remove monitoring for /path/to/vmx')
    parser.add_argument('--reset', help='Reset /path/to/vmx')
    parser.add_argument('--get-ip', help='Get IP for /path/to/vmx')
    args = parser.parse_args()

    syslog.openlog('vfused')

    monitor = VMXMonitor()

    if args.list:
        if not monitor.d.keys():
            print 'No scheduled jobs'
        for k, v in monitor.get_scheduled().items():
            print 'Monitoring: %s (%s, %s, %s)' % (v[0], v[2], v[3], k)
        for k, v in monitor.get_running().items():
            print 'Running: %s (%s)' % (k, v)

    elif args.add:
        if not monitor.vmx_is_valid(args.add):
            print 'Invalid path (must be a vmx file): %s' % args.add
            sys.exit(1)
        if not monitor.is_scheduled(args.add):
            monitor.set_start(args.add)

    elif args.remove:
        if not monitor.vmx_is_valid(args.remove):
            print 'Invalid path (must be a vmx file): %s' % args.remove
            sys.exit(1)
        if monitor.is_scheduled(args.remove):
            monitor.set_stop(args.remove)

    elif args.reset:
        if not monitor.vmx_is_valid(args.reset):
            print 'Invalid path (must be a vmx file): %s' % args.reset
            sys.exit(1)
        if monitor.is_scheduled:
            monitor.set_reset(args.reset)

    elif args.get_ip:
        print monitor.get_ip(args.get_ip)

    elif args.monitor:
        while True:
            try:
                monitor = VMXMonitor()
                for vmx in monitor.get_monitored():
                    if monitor.is_scheduled(vmx):
                        if not monitor.is_running(vmx):
                            print 'Starting: %s' % vmx
                            syslog.syslog(syslog.LOG_ALERT, 'Starting: %s' % vmx)
                            monitor.start_vmx(vmx)
                            monitor.set_running(vmx)
                    elif monitor.to_be_removed(vmx):
                        if monitor.is_running(vmx):
                            print 'Stopping: %s' % vmx
                            syslog.syslog(syslog.LOG_ALERT, 'Stopping: %s' % vmx)
                            monitor.stop_vmx(vmx)
                        monitor.remove(vmx)
                    elif monitor.to_be_reset(vmx):
                        if monitor.is_running(vmx):
                            print 'Resetting: %s' % vmx
                            syslog.syslog(syslog.LOG_ALERT, 'Resetting: %s' % vmx)
                            monitor.reset_vmx(vmx)
                        else:
                            print 'Starting: %s' % vmx
                            syslog.syslog(syslog.LOG_ALERT, 'Starting: %s' % vmx)
                            monitor.start_vmx(vmx)
                        monitor.set_running(vmx)
                time.sleep(15)
            except KeyboardInterrupt:
                print '...later!'
                sys.exit(1)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()