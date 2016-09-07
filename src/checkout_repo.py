#! /usr/bin/env python3

import os
import sys

log_file = 'cd_filtered_commit.log'
test_source_dir = 'src/test/java/'
repository = None


def process_repo(revs_tmp):
    if len(revs_tmp) == 2:
        checkout_rev(revs_tmp[0])
        new_path = cp_repository(revs_tmp[0])
        checkout_rev(revs_tmp[1])
        cp_test_source(new_path)
        return new_path
    else:
        print('args are not correct:' + revs_tmp)


def checkout_rev(rev_hash):
    command = 'git -C ' + repository + ' reset --hard ' + rev_hash
    print(command)
    os.system(command)


def cp_repository(rev_hash, new_repo_path=None):
    if new_repo_path is None:
        new_repo_path = repository[0: repository.rindex('/')] + rev_hash[0:5]
    command = 'cp -r ' + repository + ' ' + new_repo_path
    print(command)
    os.system(command)
    return new_repo_path


def cp_test_source(new_repo_path):
    if not new_repo_path.endswith('/'):
        new_repo_path += '/'
    command = 'cp -r ' + repository + test_source_dir + ' ' + new_repo_path + test_source_dir
    print(command)
    os.system(command)


def get_p_method_to_fix(method):
    method_name_start_dix = method.rindex('.')
    method_to_fix = method[method_name_start_dix + 1:len(method)]
    method_to_fix += '@'
    method_to_fix += method[0:method_name_start_dix]
    return method_to_fix


# py checkout_repo.py /Users/liushanchen/Desktop/repo/repo_commons-io/tmp/cd_filtered_commit.log
# arg1:path of cd_filtered_commit.log
if len(sys.argv) == 2:
    log_file = sys.argv[1]
while not os.path.isfile(log_file):
    log_file = input('Please input correct path of cd_filtered_commit.log:\n')

f = open(log_file, 'r')
for line in f:
    if line.endswith('.git\n'):
        repository = line[0: line.index('.git')]
        print(repository)
        continue
    if repository is not None:
        revs = line.split(';')
        new_repo = process_repo(revs[0:2])
        m_to_fix = get_p_method_to_fix(revs[2].rstrip('\n'))
        tmp_path = log_file[0:log_file.rindex('/')]
        command = 'python3 ./fixja_pre.py "' + tmp_path + '" "' + new_repo + '" "' + m_to_fix + '"'
        os.system(command)
        break
