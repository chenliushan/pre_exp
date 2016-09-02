#! /usr/bin/env python3
import os


def create_folder(target_dir):  # Create folder
    if not os.path.exists(target_dir):
        os.system('mkdir ' + target_dir)
        print('create folder '+target_dir)


create_folder('tmp')
for x in os.listdir('./'):
    if os.path.isdir(x) and x.startswith('repo_'):
        os.system('cp ' + x + '/tmp/changes.log ' + './tmp/' + x + '_change.log')
        print(x)