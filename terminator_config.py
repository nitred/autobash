"""File to update the config file of terminator to include autobash projects.

This script is not parallel programming safe since we edit files inplace.
"""
import argparse
import copy
import os
import uuid
from pprint import pprint
from shutil import copyfile

from configobj import ConfigObj

TERMINATOR_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config/terminator")
TERMINATOR_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config/terminator/config")
TERMINATOR_CONFIG_BACKUP_FILE = os.path.join(os.path.expanduser("~"), ".config/terminator/autobash_config")


def is_config_exists():
    """Check and return if config file exists."""
    # print("CONFIG_FILE: {}".format(TERMINATOR_CONFIG_FILE))
    if os.path.exists(TERMINATOR_CONFIG_FILE):
        return True
    else:
        return False


def copy_current_config_to_backup():
    """Take a copy of the current config file as backup file."""
    copyfile(TERMINATOR_CONFIG_FILE, TERMINATOR_CONFIG_BACKUP_FILE)


def remove_all_autobash_sections_from_backup():
    """Remove all autobash sections from the backup file."""
    PROFILES = 'profiles'
    LAYOUTS = 'layouts'
    AUTOBASH_STR = 'autobash-'

    config = ConfigObj(TERMINATOR_CONFIG_BACKUP_FILE)
    # remove autobash profiles
    # print("REMOVING PROFILES")
    for profile in list(config[PROFILES].keys()):  # using list to prevent iterator
        if profile.startswith(AUTOBASH_STR):
            del config[PROFILES][profile]

    # remove autobash layouts
    # print("REMOVING LAYOUTS")
    for layout in list(config[LAYOUTS].keys()):  # using list to prevent iterator
        if layout.startswith(AUTOBASH_STR):
            del config[LAYOUTS][layout]

    # pprint(config)
    config.write()


def append_autobash_sections_to_backup(project, project_dir, conda_bashrc_filename):
    """Append autobash sections to backup based on project name."""
    PROFILES = 'profiles'
    LAYOUTS = 'layouts'
    AUTOBASH_PROJECT = 'autobash-{}'.format(project)

    PROFILE_TEMPLATE = {
        'background_image': None,
        'custom_command': 'cd {} && /bin/bash --rcfile {}'.format(project_dir,
                                                                  conda_bashrc_filename),
        'use_custom_command': True,
        'login_shell': True,
        'scrollback_lines': 10000
    }

    uuid1, uuid2, uuid3, uuid4 = str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())

    LAYOUT_TEMPLATE = {'child0': {'fullscreen': 'False',
                                  'last_active_term': uuid1,
                                  'last_active_window': 'True',
                                  'maximised': 'True',
                                  'order': '0',
                                  'parent': '',
                                  'position': '1985:24',
                                  'size': ['1855', '1056'],
                                  'title': '/bin/bash',
                                  'type': 'Window'},
                       'child1': {'order': '0',
                                  'parent': 'child0',
                                  'position': '667',
                                  'ratio': '0.63446969697',
                                  'type': 'VPaned'},
                       'child2': {'order': '0',
                                  'parent': 'child1',
                                  'position': '324',
                                  'ratio': '0.490254872564',
                                  'type': 'VPaned'},
                       'child3': {'order': '0',
                                  'parent': 'child2',
                                  'position': '746',
                                  'ratio': '0.403773584906',
                                  'type': 'HPaned'},
                       'terminal4': {'order': '0',
                                     'parent': 'child3',
                                     'profile': AUTOBASH_PROJECT,
                                     'type': 'Terminal',
                                     'uuid': uuid1},
                       'terminal5': {'command': '',
                                     'directory': '',
                                     'order': '1',
                                     'parent': 'child3',
                                     'profile': AUTOBASH_PROJECT,
                                     'type': 'Terminal',
                                     'uuid': uuid2},
                       'terminal6': {'command': '',
                                     'directory': '',
                                     'order': '1',
                                     'parent': 'child2',
                                     'profile': AUTOBASH_PROJECT,
                                     'type': 'Terminal',
                                     'uuid': uuid3},
                       'terminal7': {'command': '',
                                     'directory': '',
                                     'order': '1',
                                     'parent': 'child1',
                                     'profile': 'default',
                                     'type': 'Terminal',
                                     'uuid': uuid4}}

    config = ConfigObj(TERMINATOR_CONFIG_BACKUP_FILE)
    # append autobash profiles
    # print("APPEND PROFILES")
    config[PROFILES][AUTOBASH_PROJECT] = copy.deepcopy(PROFILE_TEMPLATE)

    # append autobash layouts
    # print("APPEND LAYOUTS")
    config[LAYOUTS][AUTOBASH_PROJECT] = copy.deepcopy(LAYOUT_TEMPLATE)

    # pprint(config)
    config.write()


def copy_backup_config_to_current():
    """Take a copy of the current config file as backup file."""
    copyfile(TERMINATOR_CONFIG_BACKUP_FILE, TERMINATOR_CONFIG_FILE)


def run(create_backup, project_details, use_backup):
    """Run script with arguments."""
    if not is_config_exists():
        print("TERMINATOR CONFIG: CONFIG DOES NOT EXIST... Creating a default config")
        default_config = """[global_config]
[keybindings]
[layouts]
  [[default]]
    [[[child1]]]
      parent = window0
      type = Terminal
    [[[window0]]]
      parent = ""
      type = Window
[plugins]
[profiles]
  [[default]]
    background_image = None
    scrollback_lines = 10000
"""
        os.makedirs(TERMINATOR_CONFIG_DIR)
        with open(TERMINATOR_CONFIG_FILE, 'w') as f:
            f.write(default_config)
        print("TERMINATOR CONFIG: CREATED DEFAULT CONFIG")

    if create_backup:
        copy_current_config_to_backup()
        remove_all_autobash_sections_from_backup()

    if project_details:
        project_name, project_dir, project_conda_bashrc = project_details
        append_autobash_sections_to_backup(project_name, project_dir, project_conda_bashrc)

    if use_backup:
        copy_backup_config_to_current()


def main():
    """The main file of the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--create_backup', action='store_true', dest='create_backup', default=False,
                        help='Create a new backup of terminator config and remove all previous autobash sections from it.')

    parser.add_argument('--append_backup', dest='project_details', nargs=3, default=[],
                        help=('Append project details to backup. Usage:\n'
                              '--append_backup PROJECT_NAME PROJECT_DIR PROJECT_CONDA_BASHRC'))

    parser.add_argument('--use_backup', action='store_true', dest='use_backup', default=False,
                        help='Copy backup in its current state as the new terminator config file.')

    results = parser.parse_args()
    create_backup, project_details, use_backup = results.create_backup, results.project_details, results.use_backup

    # print('create_backup   =', create_backup)
    # print('project_details =', project_details)
    # print('use_backup      =', use_backup)

    run(create_backup, project_details, use_backup)


if __name__ == "__main__":
    main()
