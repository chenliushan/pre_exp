#! /usr/bin/env python3
import os
import sys

p_JDKDir = 'JDKDir'
p_LogFile = 'LogFile'
p_LogLevel = 'LogLevel'
p_ProjectRootDir = 'ProjectRootDir'
p_ProjectSourceDir = 'ProjectSourceDir'
p_ProjectOutputDir = 'ProjectOutputDir'
p_ProjectLib = 'ProjectLib'
p_ProjectTestSourceDir = 'ProjectTestSourceDir'
p_ProjectTestOutputDir = 'ProjectTestOutputDir'
p_MethodToFix = 'MethodToFix'

p_sep = ' = '

p_default_JDKDir = '/Library/Java/JavaVirtualMachines/jdk1.8.0_31.jdk/Contents/Home'
p_default_sub_LogFile = '/tmp/logs/test.log'
p_default_LogLevel = 'DEBUG'
p_default_ProjectSourceDir = 'src/main/java'
p_default_ProjectTestSourceDir = 'src/test/java'
p_default_sub_ProjectTestOutputDir = 'out/test'
p_default_sub_ProjectOutputDir = 'out/production'

property_file_name = 'fixja.properties'
fixja_jar = '/Users/liushanchen/IdeaProjects/fixja/build/libs/fixja-all.jar'
arg_propery = '--FixjaSettingFile'
property_file_path = None
target_repo_path = None
target_repo_name = None
method_to_fix = None


# arg1:properties file path
# arg2:repository path
# arg3:method to fix
# 寻找properties file
# 如果找不到,自动生成 properties file
# 如果找到了,直接运行fixja

def append_path(pre, post):
    if post.startswith(os.sep):
        post = post[1:len(post)]
    if pre.endswith(os.sep):
        pre += post
    else:
        pre += (os.sep + post)
    return pre


def get_repo_name(repo_path):  # get repository's name from the git url
    start = repo_path.rindex('/')
    end = len(repo_path)
    return repo_path[start + 1:end + 1]


def get_mvn_dependencies(repo_path):
    pom_path = append_path(repo_path, 'pom.xml')
    if not os.path.isfile(pom_path):
        print('cannot locate pom.xml :' + pom_path)
        sys.exit()
    os.system('mvn -f ' + pom_path + ' dependency:copy-dependencies')
    dependency_path = append_path(repo_path, 'target/dependency')
    dependencies = ''
    for x in os.listdir(dependency_path):
        x = append_path(dependency_path, x)
        if os.path.isfile(x) and x.endswith('.jar'):
            dependencies += (x + os.pathsep)
    return dependencies[0:len(dependencies)-1]


def generate_properties_file(file_path, repository_path, fix_method):
    if os.path.isfile(file_path):
        print(file_path + ' properties file is exist.')
        return file_path
    if not file_path.endswith('.properties'):
        file_path = append_path(file_path, property_file_name)
    print(file_path)

    prop_file = open(file_path, 'w')
    content = p_JDKDir + p_sep + p_default_JDKDir + os.linesep + \
              p_LogFile + p_sep + append_path(repository_path, p_default_sub_LogFile) + os.linesep + \
              p_LogLevel + p_sep + p_default_LogLevel + os.linesep + \
              p_ProjectRootDir + p_sep + repository_path + os.linesep + \
              p_ProjectSourceDir + p_sep + p_default_ProjectSourceDir + os.linesep + \
              p_ProjectTestSourceDir + p_sep + p_default_ProjectTestSourceDir + os.linesep + \
              p_default_sub_ProjectOutputDir + p_sep + append_path(p_default_sub_ProjectOutputDir
                                                                   , target_repo_name) + os.linesep + \
              p_default_sub_ProjectTestOutputDir + p_sep + append_path(p_default_sub_ProjectTestOutputDir
                                                                       , target_repo_name) + os.linesep + \
              p_MethodToFix + p_sep + fix_method + os.linesep + \
              p_ProjectLib + p_sep + get_mvn_dependencies(repository_path) + os.linesep

    prop_file.write(content)
    prop_file.close()
    return file_path


def run_fixja(properties_file):
    command = 'java -jar ' + fixja_jar + ' ' + arg_propery + ' ' + properties_file
    os.system(command)
    pass


if len(sys.argv) == 4:
    property_file_path = sys.argv[1]
    target_repo_path = sys.argv[2]
    method_to_fix = sys.argv[3]
if property_file_path is None:
    property_file_path = input('Please input the properties file path:\n')
if method_to_fix is None:
    method_to_fix = input('Please input the method to fix:\n'
                          'eg:  finalize()@org.apache.commons.fileupload.disk.DiskFileItem\n')
while target_repo_path is None or not os.path.isdir(target_repo_path):
    target_repo_path = input('The target program path is not exist. Please input the path:\n')

target_repo_name = get_repo_name(target_repo_path)
print(target_repo_name)
property_file_path = generate_properties_file(property_file_path, target_repo_path, method_to_fix)
#run_fixja(property_file_path)
# 还差跑通checkout以及本pre
# py fixja_pre.py /Users/liushanchen/Desktop/repo/repo_commons-io/tmp /Users/liushanchen/Desktop/repo/repo_commons-io/commons-io /Users/liushanchen/Desktop/repo/repo_commons-io/commons-io
#第三个参数要调整(根据由checkout得到的输入来调整)
