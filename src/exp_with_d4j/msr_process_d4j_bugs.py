#! /usr/bin/env python3
import os

# Run MSR with prepared properties files in msr_misc_path one by one
msr_jar = '/root/test/msr_test/MSR-all.jar'
arg_propery = ' --SettingFile '
msr_misc_path = '/root/test/msr_test/misc'
java8_home = '/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java'

for x in os.listdir(msr_misc_path):  # go through all children in path
    x = msr_misc_path + os.path.sep + x
    if os.path.isfile(x) and x.endswith('.properties'):
        command = java8_home + ' -jar ' + msr_jar + arg_propery + x
        print(command)
        os.system(command)
