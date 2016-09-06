#! /usr/bin/env python3
import os
import sys

p_WorkingDir = 'WorkingDir'
p_WorkingName = 'WorkingName'
p_sep = ' = '


def get_repo_name(git_url):  # get repository's name from the git url
    start = git_url.rindex('/')
    end = git_url.rindex('.')
    return git_url[start + 1:end]


def clone_repo(git_url, repo_name=None):  # clone the repository to the desired folder
    if not repo_name:
        repo_name = get_repo_name(git_url)
        repo_dir = 'repo_' + repo_name
    if not os.path.isdir(repo_dir + os.path.sep + repo_name):
        prepare_folders(repo_dir)
        os.system('git clone ' + git_url + ' ' + repo_dir + os.path.sep + repo_name)
    else:
        print('The ' + repo_name + ' repository already exist.')
    return [repo_dir, repo_name]


def prepare_folders(repo_dir):  # Prepare folder for MSR
    create_folder(repo_dir)
    create_folder(repo_dir + os.path.sep + 'tmp')
    create_folder(repo_dir + os.path.sep + 'tmp' + os.path.sep + 'tmp_gd')


def create_folder(target_dir):  # Create folder
    if not os.path.exists(target_dir):
        os.system('mkdir ' + target_dir)


def prepare_properties_file(repo_tmp):  # Create the msr properties file of this repository.
    cwd = os.getcwd()
    prop_file_dir = repo_tmp[0] + os.path.sep + 'tmp' + os.path.sep + 'msr.properties'
    if not os.path.isfile(prop_file_dir):
        prop_file = open(prop_file_dir, 'w')
        content = p_WorkingDir + p_sep + cwd + os.path.sep + repo_tmp[0] + os.linesep + \
                  p_WorkingName + p_sep + os.path.sep + repo_tmp[1]
        prop_file.write(content)
        prop_file.close()
    else:
        print('The ' + repo_tmp[1] + ' properties already exist.')
    return cwd + os.path.sep + prop_file_dir


def run_msr(prop_tmp):  # Run the msr with the properties file.
    os.system(
        'java -cp /Users/liushanchen/IdeaProjects/MSR/lib/*' + os.pathsep +
        '/Users/liushanchen/IdeaProjects/MSR/out/artifacts/msr/msr.jar' +
        ' hk.edu.polyu.comp.msr.Application ' + prop_tmp)


if len(sys.argv) == 1:
    in_git_url = input('Input the git clone url:')
else:
    in_git_url = sys.argv[1]
print(in_git_url)
repo = clone_repo(in_git_url)
prop = prepare_properties_file(repo)
run_msr(prop)
