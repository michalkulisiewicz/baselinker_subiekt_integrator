from baselinker.Baselinker import Baselinker
from config.ReadConfigFile import ReadConfigFile


class ChangeStatusBaselinker:

    def __init__(self):
        self.bs_request = Baselinker()
        self.config_file = ReadConfigFile()
        self.failed_status = self.config_file.get_failed_status()
        self.successful_status = self.config_file.get_successful_status()

    def change_status_for_failed_order(self, order_id):
        self.bs_request.change_order_status(order_id, self.failed_status)

    def change_status_for_success_order(self, order_id, dropshipping=0):
        if dropshipping == 0:
            self.bs_request.change_order_status(order_id, self.successful_status)
        else:
            self.bs_request.change_order_status(order_id, '153958')
