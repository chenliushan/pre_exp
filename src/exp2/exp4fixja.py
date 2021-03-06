#! /usr/bin/env python3
import os
import sys

from handle_d4j import checkout_repo
from msr_process_d4j_bugs import run_msr, config_msr
from prepare_fixja_properties_file import PROPERTY_FILE_NAME, generate_properties_file
from read_config import read_config_file, find_method_to_fix, tracking_all_results, CONFIG_FILE_NAME, p_JDKDir, \
    p_FixjaDir, p_D4jDir

DEFAULT_MSR_OUTPUTS = '../traversalbugs/summary'
THIS_FILE_NAME = 'exp4fixja.py'
FIXJA_ARG_PROPERY = '--FixjaSettingFile'
WORKING_REPO_DIR = '../buggy_repo'
PROPERTY_FILES = '../property_files'
MSR_MISC = '../msr/misc'
TRACKING_RESULTS = '../results'
STR_EXAMPLE = 'Example: exp4fixja.py '

COMMAND_RUN = '-run'
COMMAND_RUN_DESC = 'Run fixja to fix specific bug (repository name and bug id refer to Defects4J), ' \
                   'properties file will be prepared automatically.'
COMMAND_RUN_SAMPLE = STR_EXAMPLE + COMMAND_RUN + ' Closure 33'

COMMAND_CHECKOUT_REPOSITORY = '-checkout'
COMMAND_CHECKOUT_REPOSITORY_DESC = 'Checkout target version buggy repository through Defects4J.'
COMMAND_CHECKOUT_SAMPLE = STR_EXAMPLE + COMMAND_CHECKOUT_REPOSITORY + ' closure 33'

COMMAND_SHOW_NAME = '-name'
COMMAND_SHOW_NAME_DESC = 'Display the short name of repositories and corresponding fully name.'
COMMAND_SHOW_NAME_SAMPLE = STR_EXAMPLE + COMMAND_SHOW_NAME

COMMAND_SHOW_CONFIG = '-expConfig'
COMMAND_SHOW_CONFIG_DESC = 'Display the configuration file dir for experiment and its contents.'
COMMAND_SHOW_CONFIG_SAMPLE = STR_EXAMPLE + COMMAND_SHOW_CONFIG

COMMAND_CLEAR = '-clear'
COMMAND_CLEAR_DESC = 'Remove all fixja output'
COMMAND_CLEAR_SAMPLE = STR_EXAMPLE + COMMAND_CLEAR

COMMAND_GENERATE = '-newFJConfig'
COMMAND_GENERATE_DESC = 'Generate a new fixja property file from an existing one'
COMMAND_GENERATE_SAMPLE = STR_EXAMPLE + COMMAND_GENERATE + ' ./fixja.properties'

COMMAND_RUN_MSR = '-runMSR'
COMMAND_RUN_MSR_DESC = 'Run msr. (If there are MSR output already, no need to run it again)'
COMMAND_RUN_MSR_SAMPLE = STR_EXAMPLE + COMMAND_RUN_MSR

COMMAND_CONFIG_MSR = '-configMSR'
COMMAND_CONFIG_MSR_DESC = 'generate the property file for MSR.'
COMMAND_CONFIG_MSR_SAMPLE = STR_EXAMPLE + COMMAND_CONFIG_MSR

COMMAND_TRACK_RESULTS = '-trackResult'
COMMAND_TRACK_RESULTS_DESC = 'Copy all newest results into \'Results\' folder'
COMMAND_TRACK_RESULTS_SAMPLE = STR_EXAMPLE + COMMAND_CONFIG_MSR

repositories = {'Closure': 'closure-compiler',
                'Lang': 'commons-lang',
                'Math': 'commons-math',
                'Time': 'joda-time',
                'Chart': 'JFreechart',
                'Mockito': 'mockito'}

expConfig = {}
script_path = ''


def print_help_msg():
    print("Help MSG:")
    print(COMMAND_RUN, COMMAND_RUN_DESC, COMMAND_RUN_SAMPLE, '\n', sep='\n')
    print(COMMAND_CHECKOUT_REPOSITORY, COMMAND_CHECKOUT_REPOSITORY_DESC, COMMAND_CHECKOUT_SAMPLE, '\n', sep='\n')
    print(COMMAND_SHOW_NAME, COMMAND_SHOW_NAME_DESC, COMMAND_SHOW_NAME_SAMPLE, '\n', sep='\n')
    print(COMMAND_SHOW_CONFIG, COMMAND_SHOW_CONFIG_DESC, COMMAND_SHOW_CONFIG_SAMPLE, '\n', sep='\n')
    # print(COMMAND_CLEAR, COMMAND_CLEAR_DESC, COMMAND_CLEAR_SAMPLE, '\n', sep='\n')
    # print(COMMAND_GENERATE, COMMAND_GENERATE_DESC, COMMAND_GENERATE_SAMPLE, '\n', sep='\n')
    print(COMMAND_RUN_MSR, COMMAND_RUN_MSR_DESC, COMMAND_RUN_MSR_SAMPLE, '\n', sep='\n')
    print(COMMAND_CONFIG_MSR, COMMAND_CONFIG_MSR_DESC, COMMAND_CONFIG_MSR_SAMPLE, '\n', sep='\n')
    print(COMMAND_TRACK_RESULTS, COMMAND_TRACK_RESULTS_DESC, COMMAND_TRACK_RESULTS_SAMPLE, '\n', sep='\n')
    print("NOTE: The Java-home should be configured as Java7 to be compatible with Defects4J.")


def show_config():
    print("Config file path: ", os.path.abspath(script_path))
    print("Config: ", expConfig)


def clear():
    pass


def run_fixja(jdk_path, fixja_path, repo_name, bug_id, d4j_path):
    repository_path = os.path.join(WORKING_REPO_DIR, repositories[repo_name] + bug_id)
    if not os.path.isdir(repository_path):
        checkout_repo(WORKING_REPO_DIR, repo_name, repositories[repo_name], bug_id, expConfig[p_D4jDir])
    property_file_path = os.path.join(repository_path, PROPERTY_FILE_NAME)
    if not os.path.isfile(property_file_path) and \
            not get_properties_file(property_file_path, repo_name, bug_id):
        method_to_fix = find_method_to_fix(DEFAULT_MSR_OUTPUTS, repo_name, bug_id)
        print('method_to_fix:' + method_to_fix)
        print('repository_path:' + repository_path)
        generate_properties_file(repository_path, method_to_fix, d4j_path, jdk_path)
    else:
        print('Info: Using existing properties file.')
    run_(jdk_path, fixja_path, property_file_path)


def get_properties_file(property_file_path, repo_name, bug_id):
    file_name = 'fixja-' + repositories[repo_name] + bug_id + '.properties'
    file = os.path.join(PROPERTY_FILES, file_name)
    if os.path.isfile(file):
        command = 'cp ' + file + ' ' + property_file_path
        print(command)
        os.system(command)
        return 1
    return 0


def run_(jdk_path, fixja_path, properties_file):
    command = jdk_path + 'bin' + os.sep + 'java -jar ' + \
              fixja_path + ' ' + FIXJA_ARG_PROPERY + ' ' + properties_file
    print(command)
    os.system(command)


def generate_another_properties_file():
    pass


def init_script_path():
    py_path = os.path.join(os.getcwd(), sys.argv[0])
    script_path = py_path[0:py_path.index(THIS_FILE_NAME)]
    return script_path


print(sys.argv)
script_path = init_script_path()
expConfig = read_config_file(os.path.join(script_path, CONFIG_FILE_NAME))
os.chdir(script_path)
if len(sys.argv) == 1:
    print_help_msg()
elif len(sys.argv) == 2:
    if sys.argv[1] == COMMAND_SHOW_CONFIG:
        show_config()
    elif sys.argv[1] == COMMAND_SHOW_NAME:
        print(repositories)
    elif sys.argv[1] == COMMAND_CLEAR:
        clear()
    elif sys.argv[1] == COMMAND_RUN_MSR:
        run_msr(MSR_MISC)
    elif sys.argv[1] == COMMAND_CONFIG_MSR:
        config_msr(MSR_MISC)
    elif sys.argv[1] == COMMAND_TRACK_RESULTS:
        print('Processing ...')
        tracking_all_results(WORKING_REPO_DIR, TRACKING_RESULTS)
    else:
        print_help_msg()
elif len(sys.argv) == 4:
    if sys.argv[1] == COMMAND_RUN:
        run_fixja(expConfig[p_JDKDir], expConfig[p_FixjaDir], sys.argv[2], sys.argv[3], expConfig[p_D4jDir])

    elif sys.argv[1] == COMMAND_CHECKOUT_REPOSITORY:
        checkout_repo(WORKING_REPO_DIR, sys.argv[2], repositories[sys.argv[2]], sys.argv[3], expConfig[p_D4jDir])

    elif sys.argv[1] == COMMAND_GENERATE:
        generate_another_properties_file()

    else:
        print_help_msg()
else:
    print_help_msg()
