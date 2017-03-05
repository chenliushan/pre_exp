import os

from my_util import append_path

CONFIG_FILE_NAME = 'fixja_exp.properties'

p_JDKDir = 'JDKDir'
p_FixjaDir = 'FixjaDir'
p_D4jDir = 'D4jDir'


def read_config_file(config_path):  # Reading configuration for this script
    if os.path.isfile(config_path) and config_path.endswith(CONFIG_FILE_NAME):
        config_dict = {}
        with open(config_path, 'r') as file:
            for line in file:
                if line.startswith(p_JDKDir):
                    config_dict[p_JDKDir] = line[line.index('=') + 1:].strip()
                if line.startswith(p_FixjaDir):
                    config_dict[p_FixjaDir] = line[line.index('=') + 1:].strip()
                if line.startswith(p_D4jDir):
                    config_dict[p_D4jDir] = line[line.index('=') + 1:].strip()
    return config_dict


D4J_BUILD_FILE_NAME = 'defects4j.build.properties'

D4J_BUG_ID = 'd4j.bug.id'
D4J_CLASSES_MODIFIED = 'd4j.classes.modified'
D4J_DIR_SRC_CLASSES = 'd4j.dir.src.classes'
D4J_DIR_SRC_TESTS = 'd4j.dir.src.tests'
D4J_PROJECT_ID = 'd4j.project.id'
D4J_TESTS_TRIGGER = 'd4j.tests.trigger'


def read_d4j_config_file(repo_path):  # Reading d4j build file of the target vesion program
    config_path = append_path(repo_path, D4J_BUILD_FILE_NAME)
    if os.path.isfile(config_path):
        config_dict = {}
        with open(config_path, 'r') as file:
            for line in file:
                if line.startswith(D4J_BUG_ID):
                    config_dict[D4J_BUG_ID] = line[line.index('=') + 1:].strip()
                if line.startswith(D4J_CLASSES_MODIFIED):
                    config_dict[D4J_CLASSES_MODIFIED] = line[line.index('=') + 1:].strip()
                if line.startswith(D4J_DIR_SRC_CLASSES):
                    config_dict[D4J_DIR_SRC_CLASSES] = line[line.index('=') + 1:].strip()
                if line.startswith(D4J_DIR_SRC_TESTS):
                    config_dict[D4J_DIR_SRC_TESTS] = line[line.index('=') + 1:].strip()
                if line.startswith(D4J_PROJECT_ID):
                    config_dict[D4J_PROJECT_ID] = line[line.index('=') + 1:].strip()
                if line.startswith(D4J_TESTS_TRIGGER):
                    config_dict[D4J_TESTS_TRIGGER] = line[line.index('=') + 1:].strip()
    return config_dict


def find_method_to_fix(msr_output_path, repo_full_name, bug_id):  # Finding the target method from msr outputs
    for x_file in os.listdir(msr_output_path):  # go through all children in path
        x_file = msr_output_path + os.path.sep + x_file
        if x_file.startswith(repo_full_name) and os.path.isfile(x_file) and x_file.endswith('.log'):
            with open(x_file, 'r') as file:
                for line in file:
                    bug_unit = line.strip().split(';')
                    if bug_unit[0] == bug_id:
                        print(bug_unit)
                        return bug_unit[2]
