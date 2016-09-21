#! /usr/bin/env python3
import os
import shutil
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
p_ProjectTestsToInclude = 'ProjectTestsToInclude'
p_ProjectTestsToExclude = 'ProjectTestsToExclude'
p_ProjectExtraClasspath = 'ProjectExtraClasspath'
p_ProjectCompilationCommand = 'ProjectCompilationCommand'
p_ProjectExecutionCommand = 'ProjectExecutionCommand'
p_MethodToFix = 'MethodToFix'
p_Encoding = 'Encoding'

p_sep = ' = '

p_default_JDKDir = '/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java'
p_default_JDKDir_mac = '/Library/Java/JavaVirtualMachines/jdk1.8.0_31.jdk/Contents/Home'
p_default_sub_LogFile = '/fixja.log'
p_default_LogLevel = 'DEBUG'
p_default_ProjectSourceDir = 'src/main/java'
p_default_ProjectTestSourceDir = 'src/test/java'
p_default_sub_ProjectTestOutputDir = 'out/test'
p_default_sub_ProjectOutputDir = 'out/production'
p_default_Encoding = 'ISO-8859-1'

property_file_name = 'fixja.properties'
fixja_jar = './fixja-all.jar'
arg_propery = '--FixjaSettingFile'
property_file_path = None
target_repo_path = None
target_repo_name = None
method_to_fix = None


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
    return dependencies[0:len(dependencies) - 1]


def generate_properties_file(file_path, repository_path, fix_method):  # generate fixja properties file
    if not file_path.endswith('.properties'):
        file_path = append_path(file_path, property_file_name)
    print(file_path)

    if os.path.isfile(file_path):  # Skip if there is a properties file.
        print(file_path + ' properties file is exist.')
        return file_path

    tmp_cp = ''
    if cp is not None and os.path.isfile(cp):
        tmp_cont = open(cp, 'r').read().split(os.pathsep)
        for line in tmp_cont:
            if 'classes' not in line and '/target/tests' not in line:
                if line.endswith('junit-4.7.jar'):
                    tmp_cp += '/root/test/defects4j_test/defects4j/framework/lib/junit-4.12.jar' + os.pathsep
                else:
                    if os.path.isfile(line):
                        tmp_cp += line + os.pathsep
                    else:
                        print('classpath: ' + line + ' is not exist!!')
                        os._exit(1)
        tmp_cp = tmp_cp[0:len(tmp_cp) - 1]
    else:
        tmp_cp = get_mvn_dependencies(repository_path)

    tmp_test_to_include = ''
    if test_to_include is not None and os.path.isfile(test_to_include):
        tmp_cont = open(test_to_include, 'r')
        for line in tmp_cont:
            tmp_test_to_include += (line.strip() + os.pathsep)
        tmp_test_to_include = tmp_test_to_include[0:len(tmp_test_to_include) - 1]
        tmp_cont.close()

    if '@' not in fix_method:
        fix_method = get_p_method_to_fix(fix_method)

    prop_file = open(file_path, 'w')
    content = p_JDKDir + p_sep + p_default_JDKDir + os.linesep + \
              p_LogFile + p_sep + append_path(repository_path, p_default_sub_LogFile) + os.linesep + \
              p_LogLevel + p_sep + p_default_LogLevel + os.linesep + \
              p_ProjectRootDir + p_sep + repository_path + os.linesep + \
              p_ProjectSourceDir + p_sep + p_default_ProjectSourceDir + os.linesep + \
              p_ProjectTestSourceDir + p_sep + p_default_ProjectTestSourceDir + os.linesep + \
              p_ProjectOutputDir + p_sep + append_path(p_default_sub_ProjectOutputDir
                                                       , target_repo_name) + os.linesep + \
              p_ProjectTestOutputDir + p_sep + append_path(p_default_sub_ProjectTestOutputDir
                                                           , target_repo_name) + os.linesep + \
              p_MethodToFix + p_sep + fix_method + os.linesep + \
              p_ProjectTestsToInclude + p_sep + tmp_test_to_include + os.linesep + \
              p_ProjectTestsToExclude + p_sep + os.linesep + \
              p_ProjectExtraClasspath + p_sep + os.linesep + \
              p_ProjectCompilationCommand + p_sep + os.linesep + \
              p_ProjectExecutionCommand + p_sep + os.linesep + \
              p_Encoding + p_sep + p_default_Encoding + os.linesep + \
              p_ProjectLib + p_sep + tmp_cp + os.linesep

    prop_file.write(content)
    prop_file.close()
    return file_path


def get_p_method_to_fix(method):
    method_name_start_dix = method.rindex('.')
    method_to_fix = method[method_name_start_dix + 1:len(method)]
    method_to_fix += '@'
    method_to_fix += method[0:method_name_start_dix]
    return method_to_fix


def run_fixja(properties_file):
    command = '/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -jar ' + \
              fixja_jar + ' ' + arg_propery + ' ' + properties_file
    os.system(command)


def generate_another_properties(file_path):
    new_file = file_path.replace('fixja.', 'fixja1.')
    # shutil.copyfile(file_path, new_file)
    another = open(new_file, 'w')
    file = open(file_path, 'r')
    content = file.read()
    new_content=content.replace('/root', '/Users/liushanchen/Desktop')
    another.write(new_content.replace(p_default_JDKDir,p_default_JDKDir_mac))
    another.close()


# def get_content(file_path):
#     f = open(file_path, 'r')
#     content = f.read()
#     f.close()
#     return content




# input:
# arg1:properties file path
# arg2:repository path
# arg3:method to fix
# arg4:path of file that contain testsToInclude (tests.relevant exported by d4j)
# arg5:path of file that contain cp (cp.test exported by d4j)
# 寻找properties file
# 如果找不到,自动生成 properties file
# 如果找到了,直接运行fixja

if len(sys.argv) == 6:
    property_file_path = sys.argv[1]
    target_repo_path = sys.argv[2]
    method_to_fix = sys.argv[3]
    test_to_include = sys.argv[4]
    cp = sys.argv[5]
if property_file_path is None:
    property_file_path = input('Please input the properties file path:\n')
if method_to_fix is None:
    method_to_fix = input('Please input the method to fix:\n'
                          'eg:  finalize()@org.apache.commons.fileupload.disk.DiskFileItem\n')
while target_repo_path is None or not os.path.isdir(target_repo_path):
    target_repo_path = input('The target program path is not exist. Please input the path:\n')

while test_to_include is None:
    test_to_include = input('The TestsToInclude file is not exist. Please input the path:\n')

while cp is None:
    cp = input('The cp file is not exist. Please input the path:\n')

target_repo_name = get_repo_name(target_repo_path)
property_file_path = generate_properties_file(property_file_path, target_repo_path, method_to_fix)
run_fixja(property_file_path)
generate_another_properties(property_file_path)
