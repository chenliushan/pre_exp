#! /usr/bin/env python3
import os

git_url_path = './git_path.txt'
f = open(git_url_path, 'r')

for line in f:
    os.system('python3 ./pre_exp.py ' + line)

print('Done')
