from baselinker.Baselinker import Baselinker
from subiekt.SubiektApiRequests import SubiektApiRequests
from baselinker.ChangeStatusBaselinker import ChangeStatusBaselinker
from dropshipping.ParseBSOrderToSubiektOrderDropshipping import ParseBSOrderToSubiektOrderDropshipping
from config.ReadConfigFile import ReadConfigFile


class DropshippngOrders:

    def __init__(self, subiekt_api_key):
        self.subiekt_api_key = subiekt_api_key
        self.change_status_baselinker = ChangeStatusBaselinker()
        self.baselinker = Baselinker()
        self.subiekt_api_requests = SubiektApiRequests(self.subiekt_api_key)
        self.added_orders = {}
        self.failed_orders = {}
        self.config_file = ReadConfigFile()
        self.dropshipping_status = self.config_file.get_dropshipping_status()

    def calculate_price(self):
        customer_price = float(input('customer paid: '))
        price = customer_price
        print('Final price = {}'.format(price))
        return round(price, 2)

    def get_order_list_from_bs(self):
        orders_bs_list = self.baselinker.get_orders_from_status(self.dropshipping_status)
        return orders_bs_list

    def get_order_id(self, order_bs):
        order_id = order_bs['order_id']
        return str(order_id)

    def get_order_ref(self, subiekt_add_order_response):
        order_ref = subiekt_add_order_response['data']['order_ref']
        return order_ref

    def get_success_order_details(self, order_id, subiekt_add_order_response):
        data = {}
        order_ref = self.get_order_ref(subiekt_add_order_response)
        data['order_ref'] = order_ref
        self.added_orders[order_id] = data

    def get_failed_order_details(self, order_id, failed_orders, subiekt_add_order_response):
        data = {}
        message = subiekt_add_order_response['message']
        data['order_ref'] = 'none'
        data['order_id'] = order_id
        data['message'] = message
        failed_orders[order_id] = data
        return failed_orders

    def get_parsed_order_list(self):
        orders_bs_list = self.get_order_list_from_bs()
        for orders_bs in orders_bs_list:
            print('Information about order id: {}'.format(self.get_order_id(orders_bs)))
            price = self.calculate_price()
            parse_order = ParseBSOrderToSubiektOrderDropshipping(price)
            subiekt_order = parse_order.parse(orders_bs)
            subiekt_add_order_response = self.subiekt_api_requests.add_order_subiekt(subiekt_order)

            if subiekt_add_order_response['state'] == 'success':
                order_id = self.get_order_id(orders_bs)
                order_ref = self.get_order_ref(subiekt_add_order_response)
                print('Order {} created as: {}'.format(order_id, order_ref))
                self.get_success_order_details(order_id, subiekt_add_order_response)

            else:
                print('Order id: {}. Cannot be created'.format(orders_bs['order_id']))
                order_id = self.get_order_id(orders_bs)
                failed_orders = self.get_failed_order_details(order_id, failed_orders, subiekt_add_order_response)
                self.change_status_baselinker.change_status_for_failed_order(order_id)

        return self.added_orders
