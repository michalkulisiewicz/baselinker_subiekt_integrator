from subiekt.SubiektApiRequests import SubiektApiRequests
import json
from baselinker.ChangeStatusBaselinker import ChangeStatusBaselinker
from log.setup_logger import logger


class SubiektMakeSaleDoc:
    def __init__(self, added_orders, subiekt_api_key):
        self.subiekt_api_key = subiekt_api_key
        self.subiekt_api = SubiektApiRequests(self.subiekt_api_key)
        self.added_orders = added_orders
        self.change_status_baselinker = ChangeStatusBaselinker()

    def make_sale_doc_json(self, order_ref):
        sale_doc = {}
        data = {}
        sale_doc['api_key'] = self.subiekt_api_key
        data['order_ref'] = order_ref
        sale_doc['data'] = data
        return json.dumps(sale_doc, ensure_ascii=False)

    def successfully_converted(self, sale_doc, order_id):
        doc_ref = sale_doc['data']['doc_ref']
        self.added_orders[order_id]['doc_ref'] = doc_ref
        self.change_status_baselinker.change_status_for_success_order(order_id)

    def try_convert_zk_to_sale_doc(self, sale_doc_json, order_id):
        sale_doc = self.subiekt_api.make_sale_doc(sale_doc_json)
        print(sale_doc)
        logger.info(sale_doc)
        if sale_doc['data']['doc_state_code'] == 0:
            self.successfully_converted(sale_doc, order_id)
        else:
            self.change_status_baselinker.change_status_for_failed_order(order_id)
            pass

    def make_sale_doc(self):
        for key, value in self.added_orders.items():
            order_ref = value['order_ref']
            sale_doc_json = self.make_sale_doc_json(order_ref)
            order_id = key
            self.try_convert_zk_to_sale_doc(sale_doc_json, order_id)
        return self.added_orders
