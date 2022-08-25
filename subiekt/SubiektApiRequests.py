import requests
import json

class SubiektApiRequests():

    def __init__(self, subiekt_api_key):
        self.headers = {'Content-Type': 'application/json;charset=utf-8'}
        self.subiekt_api_key = subiekt_api_key

    def add_order_subiekt(self, order):

        url = 'http://127.0.0.1/api-subiekt-gt/public/api/order/add'

        response = requests.post( url=url, headers=self.headers, data = order.encode('utf-8') ).json()

        print(response)

        return response

    def make_sale_doc(self, data):

        url = 'http://127.0.0.1/api-subiekt-gt/public/api/order/makesaledoc'

        response = requests.post( url = url, headers = self.headers, data = data.encode('utf-8') ).json()

        return response

    def create_get_document_dict(self, doc_ref):
        document = {}
        document['api_key'] = self.subiekt_api_key
        data = {}
        document['data'] = data
        document['data']['doc_ref'] = doc_ref
        document = json.dumps(document)
        return document

    def get_document(self, document):
        url = 'http://127.0.0.1/api-subiekt-gt/public/api/document/get'

        document = self.create_get_document_dict('PA 1/2019')
        response = requests.post(url=url, headers=self.headers, data=document.encode('utf-8') ).json()

        return response


