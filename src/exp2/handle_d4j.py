#! /usr/bin/env python3
import os

from my_util import cp_repo

RELEVANT_TESTS_FILE_NAME = 'out_relevant_tests.txt'
CP_TEST_FILE_NAME = 'out_cp.txt'
# REPO_FOLDER_NAME = 'buggy_repo'
TMP_REPO_DIR = '/tmp/'


def checkout_repo(target_folder, repo_name, repo_full_name, bug_id, d4j_path):
    repo_path = os.path.join(TMP_REPO_DIR, repo_full_name + bug_id)
    command = d4j_path + ' checkout -p ' + repo_name + \
              ' -v ' + bug_id + 'b -w ' + repo_path
    print(command)
    os.system(command)
    return cp_repo(repo_path, target_folder)


def exporting_test(working_path, d4j_path):
    save_dir = os.getcwd()
    output = os.path.join(working_path, RELEVANT_TESTS_FILE_NAME)
    if not os.path.isfile(output):
        os.chdir(working_path)
        command = d4j_path + ' export -p tests.relevant -o ' + output
        print(command)
        os.system(command)
    else:
        print('Warn: Exporting_cp not executed, ' + output + ' is exist.')
    os.chdir(save_dir)
    return output


def exporting_cp(working_path, d4j_path):
    save_dir = os.getcwd()
    output = os.path.join(working_path, CP_TEST_FILE_NAME)
    if not os.path.isfile(output):
        os.chdir(working_path)
        command = d4j_path + ' export -p cp.test -o ' + output
        print(command)
        os.system(command)
    else:
        print('Warn: Exporting_test not executed,' + output + ' is exist.')
    os.chdir(save_dir)
    return output
