import json


#
# Configuration file, run to configure application or edit config.json manually
#


def show_introduction():
    print(
        'If thats your first time running the application or you have to change configuration you can follow the '
        'instruction or edit config.json manually.')


def create_list_of_statuses():
    string_of_statuses = input(
        'Input ids of statuses from baselinker that you want to import orders from. Seperate each id with comma (ex. '
        '23132,23131,23134) [note:do not put dropshipping status id]: ')
    list_of_statuses = create_list(string_of_statuses)
    return list_of_statuses


def create_list(list_of_statuses):
    list_of_statuses = list_of_statuses.split(',')
    list_of_statuses_removed_white_space = []
    for id in list_of_statuses:
        white_space_not_in_string = id.isspace()
        if not white_space_not_in_string:
            id = id.strip()
        list_of_statuses_removed_white_space.append(int(id))
    list_of_statuses = list_of_statuses_removed_white_space
    return list_of_statuses


def create_config_dict():
    config_dict = {}
    config = {}
    config_dict['config'] = config

    config['list_of_statuses'] = create_list_of_statuses()
    config['dropshipping_status'] = int(input('Input order id of dropshipping status: '))
    config['failed_status'] = int(input('Input order id of status to move orders that could not be added to subiekt: '))
    config['successful_status'] = int(input('Input order id of status that were successfully added  to subiekt: '))
    config['ui_path_robot_location'] = input(
        'Input location of UiRobot.exe [ex: C:\\Users\\USERNAME\\AppData\\Local\\UiPath\\app-VERSION-NUMBER\\UiRobot'
        '.exe]: ')
    config['baselinker_token'] = input('Input token for baselinker api: ')
    config['subiekt_api_key'] = input('Input api key for subiekt: ')
    config['test_document'] = input('Input name of test document existing in subiekt in order to check connection [ex: PA 1/2019]')
    return config_dict


def save_config_to_file(config_dict):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, ensure_ascii=False)


def run():
    show_introduction()
    config_dict = create_config_dict()
    save_config_to_file(config_dict)


run()
