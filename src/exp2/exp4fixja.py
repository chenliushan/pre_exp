#! /usr/bin/env python3
import os
import sys

from handle_d4j import checkout_repo
from my_util import append_path
from prepare_fixja_properties_file import PROPERTY_FILE_NAME, generate_properties_file
from read_config import read_config_file, find_method_to_fix

DEFAULT_CONFIG_FILE = './fixja_exp.properties'
p_JDKDir = 'JDKDir'
p_FixjaDir = 'FixjaDir'
p_D4jDir = 'D4jDir'

FIXJA_ARG_PROPERY = '--FixjaSettingFile'

STR_EXAMPLE = 'Example: '

COMMAND_RUN = '-run'
COMMAND_RUN_DESC = 'Run fixja to fix specific bug (repository name and bug id refer to Defects4J), ' \
                   'properties file will be prepared automatically.'
COMMAND_RUN_SAMPLE = STR_EXAMPLE + COMMAND_RUN + ' closure 33'

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

COMMAND_RUN_MSR = '-runMSR '
COMMAND_RUN_MSR_DESC = 'Run msr. (If there are MSR output already, no need to run it again)'
COMMAND_RUN_MSR_SAMPLE = STR_EXAMPLE + COMMAND_RUN_MSR

COMMAND_CONFIG_MSR = '-configMSR '
COMMAND_CONFIG_MSR_DESC = 'generate the property file for MSR.'
COMMAND_CONFIG_MSR_SAMPLE = STR_EXAMPLE + COMMAND_CONFIG_MSR

repositories = {'Closure': 'closure-compiler',
                'Lang': 'commons-lang',
                'Math': 'commons-math',
                'Time': 'joda-time',
                'Chart': 'JFreechart',
                'Mockito': 'mockito'}


def print_help_msg():
    print("Help MSG:")
    print(COMMAND_RUN, COMMAND_RUN_DESC, COMMAND_RUN_SAMPLE, '\n', sep='\n')
    print(COMMAND_CHECKOUT_REPOSITORY, COMMAND_CHECKOUT_REPOSITORY_DESC, COMMAND_CHECKOUT_SAMPLE, '\n', sep='\n')
    print(COMMAND_SHOW_NAME, COMMAND_SHOW_NAME_DESC, COMMAND_SHOW_NAME_SAMPLE, '\n', sep='\n')
    print(COMMAND_SHOW_CONFIG, COMMAND_SHOW_CONFIG_DESC, COMMAND_SHOW_CONFIG_SAMPLE, '\n', sep='\n')
    print(COMMAND_CLEAR, COMMAND_CLEAR_DESC, COMMAND_CLEAR_SAMPLE, '\n', sep='\n')
    print(COMMAND_GENERATE, COMMAND_GENERATE_DESC, COMMAND_GENERATE_SAMPLE, '\n', sep='\n')
    print(COMMAND_RUN_MSR, COMMAND_RUN_MSR_DESC, COMMAND_RUN_MSR_SAMPLE, '\n', sep='\n')
    print(COMMAND_CONFIG_MSR, COMMAND_CONFIG_MSR_DESC, COMMAND_CONFIG_MSR_SAMPLE, '\n', sep='\n')


def show_name():
    print(repositories)


def show_config():
    print("Config file path: ", os.path.abspath(DEFAULT_CONFIG_FILE))
    print("Config: ", read_config_file(DEFAULT_CONFIG_FILE))


def clear():
    pass


def checkout(repo_name, bug_id, d4j_path):
    checkout_repo(repo_name, bug_id, d4j_path)


def run_fixja(repository_path, repo_name, bug_id, d4j_path, jdk_path, fixja_path):
    property_file_path = append_path(repository_path, PROPERTY_FILE_NAME)
    method_to_fix = find_method_to_fix(repositories[repo_name], bug_id)
    if not os.path.isfile(property_file_path):
        generate_properties_file(repository_path, method_to_fix, d4j_path, jdk_path)
    run_(jdk_path, fixja_path, property_file_path)


def run_(jdk_path, fixja_path, properties_file):
    command = jdk_path + ' -jar ' + \
              fixja_path + ' ' + FIXJA_ARG_PROPERY + ' ' + properties_file
    print(command)
    os.system(command)


def generate_another_properties_file():
    pass


print(sys.argv)
if len(sys.argv) == 1:
    print_help_msg()
elif len(sys.argv) == 2:
    if sys.argv[1] == COMMAND_SHOW_CONFIG:
        show_config()
    elif sys.argv[1] == COMMAND_SHOW_NAME:
        show_name()
    elif sys.argv[1] == COMMAND_CLEAR:
        clear()
    else:
        print_help_msg()
elif len(sys.argv) == 4:
    if sys.argv[1] == COMMAND_RUN:
        run_fixja()
    elif sys.argv[1] == COMMAND_CHECKOUT_REPOSITORY:
        checkout()
    elif sys.argv[1] == COMMAND_GENERATE:
        generate_another_properties_file()
    else:
        print_help_msg()
else:
    print_help_msg()
