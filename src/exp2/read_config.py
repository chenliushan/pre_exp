import os
from shutil import copyfile

CONFIG_FILE_NAME = 'fixja_exp.properties'

p_JDKDir = 'JDKDir'
p_FixjaDir = 'FixjaDir'
p_D4jDir = 'D4jDir'


def read_config_file(config_path):  # Reading configuration for this script
    config_dict = {}
    if os.path.isfile(config_path):
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


def read_d4j_config_file(repo_path):  # Reading d4j build file of the target version program
    config_path = os.path.join(repo_path, D4J_BUILD_FILE_NAME)
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
        if x_file.startswith(repo_full_name) and x_file.endswith('.log'):
            x_file = os.path.join(msr_output_path, x_file)
            if os.path.isfile(x_file):
                with open(x_file, 'r') as file:
                    for line in file:
                        bug_unit = line.strip().split(';')
                        if bug_unit[0] == bug_id:
                            return bug_unit[2]
    return ''


def tracking_all_results(working_dir, new_output_dir):  # Finding all the experiment results in the working dir
    for x_repo in os.listdir(working_dir):
        x_repo_dir = os.path.join(working_dir, x_repo)
        if os.path.isdir(x_repo_dir):  # go through all repo in working dir
            print('Copying ' + x_repo + ' ...')
            for folder in os.listdir(x_repo_dir):
                if folder == 'fixja_output':  # find the experiment output in repo
                    dst = os.path.join(new_output_dir, x_repo)
                    if not os.path.isdir(dst):
                        os.mkdir(dst)
                    o_output_dir = os.path.join(x_repo_dir, folder)
                    for exp_output in os.listdir(o_output_dir):
                        src = os.path.join(o_output_dir, exp_output)
                        if is_desired_size(src) and is_desired_name(exp_output):
                            copyfile(src, os.path.join(dst, exp_output))
                    break
    print('tracking_all_results is done')


def is_desired_name(file_name):
    if file_name == 'evaluated_fix_actions.log' or \
                    file_name == 'evaluated_snapshots.log' or \
                    file_name == 'monitored_states.log' or \
                    file_name == 'monitored_test_results.log' or \
                    file_name == 'fixja.log' or \
                    file_name == 'plausible_fix_actions.log' or \
                    file_name == 'raw_fix_actions.log' or \
                    file_name == 'snippets.log' or \
                    file_name == 'test_cases_files.txt':
        return 1
    return 0


def is_desired_size(path):
    if os.path.getsize(path) < 10 ** 10:
        return 1
    return 0
