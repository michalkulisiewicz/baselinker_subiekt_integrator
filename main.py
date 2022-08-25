from baselinker.Baselinker import Baselinker
from subiekt.ParseBsOrderToSubiektOrder import ParseBsOrderToSubiektOrder
from subiekt.SubiektApiRequests import SubiektApiRequests
from subiekt.SubiektMakeSaleDoc import SubiektMakeSaleDoc
from baselinker.ChangeStatusBaselinker import ChangeStatusBaselinker
from ui_path.RunUiPath import RunUiPath
from dropshipping.DropshippingOrders import DropshippngOrders
from log.setup_logger import logger
from config.ReadConfigFile import ReadConfigFile
import sys


class Run:
    def __init__(self):
        self.config_file = ReadConfigFile()
        self.subiekt_api_key = self.config_file.get_subiekt_api_key()
        self.start_message()
        self.test_connection()
        self.add_allegro_orders()

    def start_message(self):
        message = 'Script started'
        print(message)
        logger.info(message)

    def test_connection(self):
        subiekt_api_requests = SubiektApiRequests(self.subiekt_api_key)
        document = subiekt_api_requests.get_document(self.config_file.get_test_document())
        if document['state'] == 'success':
            message = 'Connection to database established'
            print(message)
            logger.info(message)
        else:
            message = 'Connection to database can not be established, Check log file.'
            print(message)
            logger.info(document['message'])
            sys.exit()

    def check_available_orders_dropshipping(self, added_orders):
        if not added_orders:
            message = 'There are no available orders for dropshipping.'
            print(message)
            logger.info(message)
            return False
        else:
            return True

    def create_sale_document(self, added_orders):
        make_sale = SubiektMakeSaleDoc(added_orders, self.subiekt_api_key)
        added_orders = make_sale.make_sale_doc()

    def get_allegro_orders_from_baselinker(self):
        baselinker = Baselinker()
        list_of_statuses = self.config_file.get_list_of_statuses()
        orders_bs_list = baselinker.get_orders_from_list_of_statuses(list_of_statuses)
        return orders_bs_list

    def check_available_orders_allegro(self, orders_bs_list):
        if not orders_bs_list:
            message = 'There are no available orders from allegro.'
            print(message)
            logger.info(message)
            return False
        else:
            return True

    def get_number_of_orders_and_print(self, orders_bs_list):
        number_of_orders = 0
        for orders in orders_bs_list:
            for order in orders:
                number_of_orders += 1
        message = 'There are {} available orders from allegro'.format(number_of_orders)
        print(message)
        logger.info(message)

    def get_list_of_sets(self):
        list_of_sets = []
        txt_file = open('subiekt/list_of_sets.txt', 'r', encoding="utf8")
        for item in txt_file:
            item = item.strip()
            list_of_sets.append(item)
        return list_of_sets

    def make_set(self, orders_bs_list):
        list_of_sets = self.get_list_of_sets()
        uipath = RunUiPath()
        for orders_bs in orders_bs_list:
            for order in orders_bs:
                for product in order['products']:
                    sku = product['sku']
                    if sku in list_of_sets:
                        qty = product['quantity']
                        uipath.create_sku_file(str(sku))
                        uipath.create_qty_file(str(qty))
                        uipath.make_set()

    def get_order_id(self, order_bs):
        order_id = order_bs['order_id']
        return str(order_id)

    def get_order_ref(self, subiekt_add_order_response):
        order_ref = subiekt_add_order_response['data']['order_ref']
        return order_ref

    def get_success_order_details(self, order_id, added_orders, subiekt_add_order_response):
        data = {}
        order_ref = self.get_order_ref(subiekt_add_order_response)
        data['order_ref'] = order_ref
        added_orders[order_id] = data
        return added_orders

    def order_added_successfully(self, order, subiekt_add_order_response, added_orders):
        order_id = self.get_order_id(order)
        order_ref = self.get_order_ref(subiekt_add_order_response)
        print('Order {} created as: {}'.format(order_id, order_ref))
        logger.info('Order {} created as: {}'.format(order_id, order_ref))
        added_orders = self.get_success_order_details(order_id, added_orders, subiekt_add_order_response)
        return added_orders

    def get_failed_order_details(self, order_id, subiekt_add_order_response):
        message_subiekt = subiekt_add_order_response['message']
        message = 'Order id: {}. Cannot be created. message: {}'.format(order_id, message_subiekt)
        print(message)
        logger.info(message)

    def order_with_error(self, order, subiekt_add_order_response):
        change_status_baselinker = ChangeStatusBaselinker()
        order_id = self.get_order_id(order)
        self.get_failed_order_details(order_id, subiekt_add_order_response)
        change_status_baselinker.change_status_for_failed_order(order_id)

    def add_dropshipping_orders(self):
        dropshipping_order = DropshippngOrders(self.subiekt_api_key)
        added_orders = dropshipping_order.get_parsed_order_list()
        orders_available = self.check_available_orders_dropshipping(added_orders)
        if orders_available:
            self.create_sale_document(added_orders)

    def add_allegro_orders(self):
        added_orders = {}
        orders_bs_list = self.get_allegro_orders_from_baselinker()
        orders_available = self.check_available_orders_allegro(orders_bs_list)
        if orders_available:
            self.get_number_of_orders_and_print(orders_bs_list)
            for orders_bs in orders_bs_list:
                for order in orders_bs:
                    parse_bs_order_to_subiekt_order = ParseBsOrderToSubiektOrder(self.subiekt_api_key)
                    subiekt_order = parse_bs_order_to_subiekt_order.parse(order)
                    subiekt_api_requests = SubiektApiRequests(self.subiekt_api_key)
                    subiekt_add_order_response = subiekt_api_requests.add_order_subiekt(subiekt_order)
                    if subiekt_add_order_response['state'] == 'success':
                        added_orders = self.order_added_successfully(order, subiekt_add_order_response, added_orders)
                    else:
                        pass
                        self.order_with_error(order, subiekt_add_order_response)

            make_sale = SubiektMakeSaleDoc(added_orders, self.subiekt_api_key)
            added_orders = make_sale.make_sale_doc()


if __name__ == '__main__':
    run = Run()
