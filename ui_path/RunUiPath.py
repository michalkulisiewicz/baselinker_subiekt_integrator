import subprocess
from config.ReadConfigFile import ReadConfigFile
import os


class RunUiPath:
    def __init__(self):
        self.config_file = ReadConfigFile()

    def create_sku_file(self, sku):
        path = os.path.join(os.path.dirname(__file__), 'sku.txt')
        with open(path, 'w') as f:
            f.write(sku)

    def create_qty_file(self, qty):
        path = os.path.join(os.path.dirname(__file__), 'qty.txt')
        with open(path, 'w') as f:
            f.write(qty)

    def make_set(self):
        ui_robot_location = self.config_file.get_ui_path_robot_location()
        ui_script_location = os.path.abspath('ui_path/MontujKomplet/Main.xaml')
        subprocess.call([ui_robot_location, "-file",  ui_script_location])

