#! /usr/bin/env python3
import os
import sys

# 1>Read the MSR output log
# 2>Checkout the buggy rev
# 3>Export tests.related and cp.test

output_relevant_tests_file = 'out_relevant_tests.txt'
output_cp_test_file = 'out_cp.txt'
repo_folder = '/buggy_repo'
repos = {'closure-compiler': 'Closure', 'commons-lang': 'Lang',
         'commons-math': 'Math', 'joda-time': 'Time',
         'JFreechart':'Chart'}


def read_and_process_log(log_path):
    if os.path.isfile(log_path) and log_path.endswith('.log'):
        repo_name = get_repo_name(log_path)
        with open(log_path, 'r') as file:
            for line in file:
                process_log_unit(line, repo_name)


def process_log_unit(log_line, repo_name):
    # the bug_unit[0] is bugID,bug_unit[1] is git revision code,bug_unit[2] is modified method
    bug_unit = log_line.strip().split(';')
    print(bug_unit)
    w_path = checkout_repo(bug_unit[0], repo_name)
    print(w_path)
    d4j_exporting(w_path)
    fixja_pre_run(cp_repo(w_path), bug_unit[2])


def fixja_pre_run(w_path, method_to_fix):
    command = 'python3 fixja_d4j_pre.py ' + \
              w_path + ' ' + \
              w_path + ' "' + \
              method_to_fix + '" ' + \
              append_path(w_path, output_relevant_tests_file) + ' ' + \
              append_path(w_path, output_cp_test_file)
    print(command)
    os.system(command)


def d4j_exporting(working_path):
    save_dir = os.getcwd()
    output = append_path(working_path, output_relevant_tests_file)
    if not os.path.isfile(output):
        os.chdir(working_path)
        command = 'defects4j export -p tests.relevant -o ' + output
        print(command)
        os.system(command)
    else:
        print(output + ' is exist.')
    output = append_path(working_path, output_cp_test_file)
    if not os.path.isfile(output):
        os.chdir(working_path)
        command = 'defects4j export -p cp.test -o ' + output
        print(command)
        os.system(command)
    else:
        print(output + ' is exist.')
    os.chdir(save_dir)


def checkout_repo(bug_id, repo_name):
    working_path = append_path('/tmp/', repo_name + bug_id)
    command = 'defects4j checkout -p ' + repos[repo_name] + \
              ' -v ' + bug_id + 'b -w ' + working_path
    print(command)
    os.system(command)

    return working_path


# commons-lang_desire_buggy.log
def get_repo_name(log_path):
    repo_name = log_path[log_path.rindex(os.path.sep) + 1:-17]
    print(repo_name)
    return repo_name


def append_path(pre, post):
    if post.startswith(os.sep):
        post = post[1:len(post)]
    if pre.endswith(os.sep):
        pre += post
    else:
        pre += (os.sep + post)
    return pre


def cp_repo(working_path):
    new_working_path = append_path('/root/test/msr_test/', repo_folder)
    if not os.path.isdir(new_working_path):
        os.mkdir(new_working_path)
    if not os.path.isdir(append_path(new_working_path, working_path[working_path.rindex('/'):len(working_path)])):
        command = 'cp -rf ' + working_path + ' ' + new_working_path
        print(command)
        os.system(command)
    return append_path(new_working_path, working_path[working_path.rindex('/'):len(working_path)])


# input:
# example:py d4j_checkout_export.py commons-lang "38;e28c95ac2ce95852add84bdf3d2d9c00ac98f5de;org.apache.commons.lang3.time.FastDateFormat.format(Calendar,StringBuffer)"
# arg1:repository name (one of the following) closure-compiler,commons-lang,commons-math,joda-time
# arg2:log_line(bug_unit) e.g.: 19;a92450e88df85d6b7a0fa53517da46286c24f53f;org.joda.time.DateTimeZone.getOffsetFromLocal(long)
if len(sys.argv) == 3:
    process_log_unit(sys.argv[2], sys.argv[1])
else:
    msr_output_path = './msr_out'
    for x in os.listdir(msr_output_path):  # go through all children in path
        x = msr_output_path + os.path.sep + x
        read_and_process_log(x)
        break
