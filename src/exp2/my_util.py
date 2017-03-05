#! /usr/bin/env python3
import os


def append_path(pre, post):
    if post.startswith(os.sep):
        post = post[1:len(post)]
    if pre.endswith(os.sep):
        pre += post
    else:
        pre += (os.sep + post)
    return pre


# the working_path point to the specific repository,
# the new working path only point to a dir to place the repository.
def cp_repo(working_path,
            new_working_path):
    if not os.path.isdir(new_working_path):
        os.mkdir(new_working_path)
    if not os.path.isdir(append_path(new_working_path, working_path[working_path.rindex('/'):len(working_path)])):
        command = 'cp -rf ' + working_path + ' ' + new_working_path
        print(command)
        os.system(command)
        os.system('rm -r '+working_path)
    return append_path(new_working_path, working_path[working_path.rindex('/'):len(working_path)])
