#! /usr/bin/env python3
import os

from handle_d4j import exporting_cp, exporting_test
from my_util import append_path
from read_config import read_d4j_config_file, D4J_DIR_SRC_CLASSES, D4J_DIR_SRC_TESTS

PROPERTY_FILE_NAME = 'fixja.properties'
FIXJA_JAR = './fixja-all.jar'
ARG_PROPERY = '--FixjaSettingFile'

p_JDKDir = 'JDKDir'
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
p_TargetJavaVersion = 'TargetJavaVersion'

p_sep = ' = '
P_DEFAULT_LOGLEVEL = 'DEBUG'
P_DEFAULT_TEST_OUTPUT_DIR = 'out/test'
P_DEFAULT_OUTPUT_DIR = 'out/production'
p_default_Encoding = 'ISO-8859-1'


def collect_classpath(repository_path, d4j_path):
    collected_classpath = ''
    program_cp = exporting_cp(repository_path, d4j_path)
    if program_cp is not None and os.path.isfile(program_cp):
        tmp_cont = open(program_cp, 'r').read().split(os.pathsep)
        for line in tmp_cont:
            if 'classes' not in line and '/target/tests' not in line:
                # if line.endswith('junit-4.7.jar'):
                if 'junit' in line:
                    collected_classpath += '/root/exp_tools/defects4j/framework/lib/junit-4.12.jar' + os.pathsep
                else:
                    if os.path.isfile(line) or os.path.isdir(line):
                        collected_classpath += line + os.pathsep
                    else:
                        print('classpath: ' + line + ' is not exist!!')
        tmp_cont.close()
        collected_classpath = collected_classpath[0:len(collected_classpath) - 1]
    return collected_classpath


def collect_test_to_include(repository_path, d4j_path):
    collected_test = ''
    test_to_include = exporting_test(repository_path, d4j_path)
    if test_to_include is not None and os.path.isfile(test_to_include):
        tmp_cont = open(test_to_include, 'r')
        for line in tmp_cont:
            collected_test += (line.strip() + os.pathsep)
        collected_test = collected_test[0:len(collected_test) - 1]
        tmp_cont.close()
    return collected_test;


def get_p_method_to_fix(method):
    method_name_start_dix = method.rindex('.')
    method_to_fix = method[method_name_start_dix + 1:len(method)]
    method_to_fix += '@'
    method_to_fix += method[0:method_name_start_dix]
    return method_to_fix


def generate_properties_file(repository_path, fix_method, d4j_path, jdk_path):  # generate fixja properties file
    property_file_path = append_path(repository_path, PROPERTY_FILE_NAME)
    print(property_file_path)

    collected_classpath = collect_classpath(repository_path, d4j_path)
    tmp_test_to_include = collect_test_to_include(repository_path, d4j_path)

    if '@' not in fix_method:
        fix_method = get_p_method_to_fix(fix_method)

    d4j_build = read_d4j_config_file(repository_path)

    prop_file = open(property_file_path, 'w')
    content = p_JDKDir + p_sep + jdk_path + os.linesep + \
              p_LogLevel + p_sep + P_DEFAULT_LOGLEVEL + os.linesep + \
              p_ProjectRootDir + p_sep + repository_path + os.linesep + \
              p_ProjectSourceDir + p_sep + d4j_build[D4J_DIR_SRC_CLASSES] + os.linesep + \
              p_ProjectTestSourceDir + p_sep + d4j_build[D4J_DIR_SRC_TESTS] + os.linesep + \
              p_ProjectOutputDir + p_sep + P_DEFAULT_OUTPUT_DIR + os.linesep + \
              p_ProjectTestOutputDir + p_sep + P_DEFAULT_TEST_OUTPUT_DIR + os.linesep + \
              p_MethodToFix + p_sep + fix_method + os.linesep + \
              p_ProjectTestsToInclude + p_sep + tmp_test_to_include + os.linesep + \
              p_ProjectTestsToExclude + p_sep + os.linesep + \
              p_ProjectExtraClasspath + p_sep + os.linesep + \
              p_ProjectCompilationCommand + p_sep + os.linesep + \
              p_ProjectExecutionCommand + p_sep + os.linesep + \
              p_Encoding + p_sep + p_default_Encoding + os.linesep + \
              p_ProjectLib + p_sep + collected_classpath + os.linesep

    prop_file.write(content)
    prop_file.close()
    return property_file_path
