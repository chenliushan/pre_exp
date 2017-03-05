#! /usr/bin/env python3
import os

from my_util import append_path, cp_repo

RELEVANT_TESTS_FILE_NAME = 'out_relevant_tests.txt'
CP_TEST_FILE_NAME = 'out_cp.txt'
# REPO_FOLDER_NAME = 'buggy_repo'
TMP_REPO_DIR = '/tmp/'
WORKING_REPO_DIR = '/root/test/msr_test/buggy_repo'


def checkout_repo(bug_id, repo_name, d4j_path):
    repo_path = append_path(TMP_REPO_DIR, repo_name + bug_id)
    command = d4j_path + ' checkout -p ' + repo_name + \
              ' -v ' + bug_id + 'b -w ' + repo_path
    print(command)
    os.system(command)
    return cp_repo(repo_path, WORKING_REPO_DIR)


def exporting_cp(working_path, d4j_path):
    save_dir = os.getcwd()
    output = append_path(working_path, RELEVANT_TESTS_FILE_NAME)
    if not os.path.isfile(output):
        os.chdir(working_path)
        command = d4j_path + ' export -p tests.relevant -o ' + output
        print(command)
        os.system(command)
    else:
        print('Warn: Exporting_cp not executed, ' + output + ' is exist.')
    os.chdir(save_dir)


def exporting_test(working_path, d4j_path):
    save_dir = os.getcwd()
    output = append_path(working_path, CP_TEST_FILE_NAME)
    if not os.path.isfile(output):
        os.chdir(working_path)
        command = d4j_path + ' export -p cp.test -o ' + output
        print(command)
        os.system(command)
    else:
        print('Warn: Exporting_test not executed,' + output + ' is exist.')
    os.chdir(save_dir)
