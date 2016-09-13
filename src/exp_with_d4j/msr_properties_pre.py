#! /usr/bin/env python3
import os

# OutputPath=/root/test/msr_test
# RepoPath=/root/test/defects4j_test/defects4j/project_repos
# Defects4jDbPath=/root/test/defects4j_test/defects4j/framework/projects/Closure/commit-db
# RepoName=closure-compiler

p_OutputPath = 'OutputPath'
v_OutputPath = '/root/test/msr_test/'
p_RepoPath = 'RepoPath'
v_RepoPath = '/root/test/defects4j_test/defects4j/project_repos'
p_Defects4jDbPath = 'Defects4jDbPath'
v_Defects4jDbPath = ['/root/test/defects4j_test/defects4j/framework/projects/Closure/commit-db',
                     '/root/test/defects4j_test/defects4j/framework/projects/Lang/commit-db',
                     '/root/test/defects4j_test/defects4j/framework/projects/Math/commit-db',
                     '/root/test/defects4j_test/defects4j/framework/projects/Time/commit-db']
p_RepoName = 'RepoName'
v_RepoName = ['closure-compiler',
              'commons-lang',
              'commons-math',
              'joda-time']

file_prefix = 'msr'
file_suffix = '.properties'
p_sep = ' = '


def generate_properties_file(repo_name, db_path):
    file_path = './' + file_prefix + repo_name + file_suffix

    prop_file = open(file_path, 'w')
    content = p_OutputPath + p_sep + v_OutputPath + os.linesep + \
              p_RepoPath + p_sep + v_RepoPath + os.linesep + \
              p_Defects4jDbPath + p_sep + db_path + os.linesep + \
              p_RepoName + p_sep + repo_name + os.linesep

    prop_file.write(content)
    prop_file.close()
    return file_path


for i in range(len(v_RepoName)):
    generate_properties_file(v_RepoName[i], v_Defects4jDbPath[i])
