#! /usr/bin/env python3

import os
import sys

log_file = 'cd_filtered_commit.log'
test_source_dir = 'src/test/java'
repository = None


def process_repo(revs_tmp):
    if len(revs_tmp) == 2:
        checkout_rev(revs_tmp[0])
        new_path = cp_repository(revs_tmp[0])
        checkout_rev(revs_tmp[1])
        cp_test_source(new_path)


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


if len(sys.argv) == 2:
    log_file = sys.argv[1]

f = open(log_file, 'r')
for line in f:
    if line.endswith('.git\n'):
        repository = line[0: line.index('.git')]
        print(repository)
        continue
    if repository is not None:
        revs = line.split(';')
        process_repo(revs)
        break
