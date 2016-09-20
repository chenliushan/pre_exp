#! /usr/bin/env python3
import os
import sys

patches_folder = None
output_path = './'
output_file_name = '_all_patches.txt'
divider = '=' * 50 + os.linesep
repo_name = None


def clone_file_content(file_path, output_file_path):
    if file_path.endswith('.src.patch'):
        out_file = open(output_file_path, 'a')
        file = open(file_path, encoding="ISO-8859-1")
        out_file.write(divider)
        out_file.write(file_path[file_path.rindex('/')+1:len(file_path)] + os.linesep)
        for line in file:
            out_file.write(line)
        out_file.close()


# get input args
if len(sys.argv) == 1:
    patches_folder = input('Input the patches path:')
    repo_name = input('Input the repo name:')
else:
    patches_folder = sys.argv[1]
    repo_name = sys.argv[2]

output_file = output_path + repo_name + output_file_name
if os.path.isfile(output_file):
    os.system('rm ' + output_file)

# go through all files in a folder
for x in os.listdir(patches_folder):
    x = patches_folder + os.path.sep + x
    clone_file_content(x, output_file)
