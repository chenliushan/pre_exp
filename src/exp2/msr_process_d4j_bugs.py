#! /usr/bin/env python3
import os
import subprocess
from my_util import append_path

# Run MSR with prepared properties files in msr_misc_path one by one
msr_jar = '/root/test/msr_test/msr/MSR-all.jar'
arg_propery = ' --SettingFile '
java8_home = '/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java'


def run_msr(msr_misc_path):
    for x in os.listdir(msr_misc_path):  # go through all children in path
        x = os.path.abspath(msr_misc_path + os.path.sep + x)
        if os.path.isfile(x) and x.endswith('.properties'):
            command = java8_home + ' -jar ' + msr_jar + arg_propery + x
            print(command)
            # os.system(command)
            print(subprocess.check_output(command, shell=True))


# OutputPath=/root/test/msr_test
# RepoPath=/root/test/defects4j_test/defects4j/project_repos
# Defects4jDbPath=/root/test/defects4j_test/defects4j/framework/projects/Closure/commit-db
# RepoName=closure-compiler

p_OutputPath = 'OutputPath'
v_OutputPath = '/root/test/msr_test/msr'
p_RepoPath = 'RepoPath'
v_RepoPath = '/root/exp_tools/defects4j/project_repos'
p_Defects4jDbPath = 'Defects4jDbPath'
v_Defects4jDbPath = ['/root/exp_tools/defects4j/framework/projects/Closure/commit-db',
                     '/root/exp_tools/defects4j/framework/projects/Lang/commit-db',
                     '/root/exp_tools/defects4j/framework/projects/Math/commit-db',
                     '/root/exp_tools/defects4j/framework/projects/Time/commit-db',
                     '/root/exp_tools/defects4j/framework/projects/Mockito/commit-db',
                     '/root/exp_tools/defects4j/framework/projects/Chart/commit-db']
p_RepoName = 'RepoName'
v_RepoName = ['closure-compiler',
              'commons-lang',
              'commons-math',
              'joda-time',
              'mockito',
              'jfreechart']

file_prefix = 'msr'
file_suffix = '.properties'
p_sep = ' = '


def generate_properties_file(repo_name, db_path, target_folder):
    file_name = file_prefix + repo_name + file_suffix
    file_path = append_path(target_folder, file_name)
    prop_file = open(file_path, 'w')
    content = p_OutputPath + p_sep + v_OutputPath + os.linesep + \
              p_RepoPath + p_sep + v_RepoPath + os.linesep + \
              p_Defects4jDbPath + p_sep + db_path + os.linesep + \
              p_RepoName + p_sep + repo_name + os.linesep

    prop_file.write(content)
    prop_file.close()
    return file_path


def config_msr(target_folder):
    for i in range(len(v_RepoName)):
        generate_properties_file(v_RepoName[i], v_Defects4jDbPath[i], target_folder)
