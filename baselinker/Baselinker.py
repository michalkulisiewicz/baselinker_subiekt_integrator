import requests
from config.ReadConfigFile import ReadConfigFile


class Baselinker:

    def __init__(self):
        self.url = 'https://api.baselinker.com/connector.php'
        self.config_file = ReadConfigFile()
        self.token = self.config_file.get_baselinker_token()

    def get_orders_from_status(self, source_status):
        params = {'token': self.token, 'method': 'getOrders', 'parameters': '{{ "storage_id": 1, "status_id": {} }}'.format(source_status)}
        orders_bs = requests.post(self.url, data=params).json()
        return orders_bs['orders']

    def get_orders_from_list_of_statuses(self, statuses_list):
        orders = []
        for status in statuses_list:
            params = {'token': self.token, 'method': 'getOrders',
                      'parameters': '{{ "storage_id": 1, "status_id": {} }}'.format(status)}
            orders_bs = requests.post(self.url, data=params).json()
            orders.append(orders_bs['orders'])
        return orders

    def change_order_status(self, order_id, status_id):
        order_id = int(order_id)
        status_id = int(status_id)

        params = {'token': self.token, 'method': 'setOrderStatus',
                  'parameters': '{"order_id": %i, "status_id": %i}' % (order_id, status_id)}

        response = requests.post(self.url, data=params)

        return response.status_code
