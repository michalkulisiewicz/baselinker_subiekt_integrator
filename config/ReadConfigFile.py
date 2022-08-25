import json
import os


class ReadConfigFile:

    def __init__(self):
        self.config_file = self.read_config_file()

    def read_config_file(self):
        path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(path, 'r') as f:
            return json.load(f)

    def get_list_of_statuses(self):
        return self.config_file['config']['list_of_statuses']

    def get_dropshipping_status(self):
        return self.config_file['config']['dropshipping_status']

    def get_failed_status(self):
        return self.config_file['config']['failed_status']

    def get_successful_status(self):
        return self.config_file['config']['successful_status']

    def get_ui_path_robot_location(self):
        return self.config_file['config']['ui_path_robot_location']

    def get_baselinker_token(self):
        return self.config_file['config']['baselinker_token']

    def get_subiekt_api_key(self):
        return self.config_file['config']['subiekt_api_key']

    def get_test_document(self):
        return self.config_file['config']['test_document']
