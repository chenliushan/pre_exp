#! /usr/bin/env python3
import os

# 1>Read the MSR output log
# 2>Checkout the buggy rev
# 3>Export tests.related and cp.test

output_relevant_tests_file = 'out_relevant_tests.txt'
output_cp_test_file = 'out_cp.txt'
repos = {'closure-compiler': 'Closure', 'commons-lang': 'Lang',
         'commons-math': 'Math', 'joda-time': 'joda-time'}


def read_log(log_path):
    if os.path.isfile(log_path) and log_path.endswith('.log'):
        repo_name = get_repo_name(log_path)
        with open(log_path, 'r') as file:
            for line in file:
                # the bug_unit[0] is bugID,bug_unit[1] is git revision code,bug_unit[2] is modified method
                bug_unit = line.strip().split(';')
                print(bug_unit)
                w_path = checkout_repo(bug_unit[0], repo_name)
                d4j_exporting(w_path)
                run_fixja(w_path, bug_unit[2])


def run_fixja(w_path, method_to_fix):
    command = 'python3 fixja_d4j_pre.py ' + \
              w_path + ' ' + \
              w_path + ' "' + \
              method_to_fix + '" ' + \
              append_path(w_path, output_relevant_tests_file) + ' ' + \
              append_path(w_path, output_cp_test_file)
    print(command)
    os.system(command)


def d4j_exporting(w_path):
    save_dir = os.getcwd()
    os.chdir(w_path)
    command = 'defects4j export -p tests.relevant -o ' + append_path(w_path, output_relevant_tests_file)
    print(command)
    os.system(command)
    command = 'defects4j export -p cp.test -o ' + append_path(w_path, output_cp_test_file)
    print(command)
    os.system(command)
    os.chdir(save_dir)


def checkout_repo(bug_id, repo_name):
    working_path = '/tmp/' + repo_name + '_' + bug_id + '_buggy'
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


msr_output_path = './'
for x in os.listdir(msr_output_path):  # go through all children in path
    x = msr_output_path + os.path.sep + x
    read_log(x)
