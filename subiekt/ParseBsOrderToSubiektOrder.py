import json


class ParseBsOrderToSubiektOrder:

    def __init__(self, subiekt_api_key):
        self.subiekt_api_key = subiekt_api_key

    def get_first_name(self, fullname):
        first_name = fullname.split(' ')
        return first_name[0]

    def get_second_name(self, fullname):
        second_name = fullname.split(' ')
        return second_name[1]

    def get_street_name(self, address):
        name = [s for s in address.split() if not s.isdigit()]
        street_name = ' '.join(name)
        return street_name

    def get_street_number(self, address):
        street_number = [int(s) for s in address.split() if s.isdigit()]
        return street_number[0]

    def get_total_amount(self, bs_order):
        # Function used to get total amount of order including shipping price
        # input: order - dictionary
        # output: amount -float

        delivery_price = bs_order['delivery_price']
        total_price = 0
        for products in bs_order['products']:
            total_price = total_price + products['price_brutto']
        amount = delivery_price + total_price
        amount = round(amount, 2)
        return amount

    def parse(self, bs_order):
        subiekt_order_data = self.parse_order_data(bs_order)
        subiekt_customer_data = self.parse_customer_data(bs_order)
        subiekt_products_data = self.parse_products_data(bs_order)
        subiekt_order_json = self.create_subiekt_order_json(subiekt_order_data,
                                                            subiekt_customer_data, subiekt_products_data)
        return subiekt_order_json

    def create_subiekt_order_json(self, subiekt_order_data, subiekt_customer_data, subiekt_products_data):
        subiekt_order = {}
        # Create final dictionary return as json
        subiekt_order['api_key'] = self.subiekt_api_key
        subiekt_order['data'] = subiekt_order_data
        subiekt_order['data']['customer'] = subiekt_customer_data
        subiekt_order['data']['products'] = subiekt_products_data
        subiekt_order_json = json.dumps(subiekt_order, ensure_ascii=False)
        return subiekt_order_json

    def parse_order_data(self, bs_order):
        subiekt_order_data = {}
        order_id = str(bs_order['order_id'])
        shipping_details = bs_order['delivery_method']
        email = bs_order['email']
        allegro_login = bs_order['user_login']
        subiekt_order_data['comments'] = '{}*{}*{}*{}*'.format(order_id, shipping_details, email, allegro_login)
        subiekt_order_data['reference'] = order_id
        subiekt_order_data['amount'] = float(self.get_total_amount(bs_order))
        subiekt_order_data['create_product_if_not_exists'] = 0
        subiekt_order_data['pay_type'] = 'transfer'
        return subiekt_order_data

    def parse_customer_data(self, bs_order):
        customer_data = {}
        order_id = bs_order['order_id']
        if bs_order['want_invoice'] == '1' and bs_order['invoice_nip'] != '':
            if bs_order['invoice_nip'] != '':
                print('Order id: {}. Invoice cannot be created, NIP field is empty. Creating receipt'.format(order_id))
            customer_data['is_company'] = 'true'
            customer_data['company_name'] = bs_order['invoice_company']
            customer_data['tax_id'] = bs_order['invoice_nip']
            customer_data['ref_id'] = bs_order['invoice_nip']
            customer_data['email'] = bs_order['email']
            if bs_order['invoice_fullname'] == '':
                customer_data['firstname'] = ''
                customer_data['lastname'] = ''
            else:
                customer_data['firstname'] = self.get_first_name(bs_order['invoice_fullname'])
                customer_data['lastname'] = self.get_second_name(bs_order['invoice_fullname'])

            if bs_order['invoice_address'] == '':
                customer_data['address'] = ''
                customer_data['address_no'] = ''
            else:
                customer_data['address'] = bs_order['invoice_address']
                customer_data['address_no'] = ''
            if bs_order['invoice_city'] == '':
                customer_data['city'] = ''
            else:
                customer_data['city'] = bs_order['invoice_city']
            if bs_order['invoice_postcode'] == '':
                customer_data['post_code'] = ''
            else:
                customer_data['post_code'] = bs_order['invoice_postcode']
        else:
            if bs_order['delivery_fullname'] == '':
                customer_data['firstname'] = ''
                customer_data['lastname'] = ''
            else:
                customer_data['firstname'] = self.get_first_name(bs_order['delivery_fullname'])
                customer_data['lastname'] = self.get_second_name(bs_order['delivery_fullname'])

            customer_data['email'] = bs_order['email']
            customer_data['address'] = bs_order['delivery_address']
            customer_data['city'] = bs_order['delivery_city']
            customer_data['post_code'] = bs_order['delivery_postcode']
            customer_data['phone'] = bs_order['phone']
            customer_data['ref_id'] = str(order_id)

        return customer_data

    def parse_products_data(self, bs_order):
        shipping = {}
        products = []
        for item in bs_order['products']:
            product = {}
            product['code'] = item['sku']
            product['price'] = float(item['price_brutto'])
            product['price_before_discount'] = float(item['price_brutto'])
            product['name'] = item['name']
            product['qty'] = str(item['quantity'])
            products.append(product)

        if bs_order['delivery_price'] != 0:
            shipping['code'] = 'PRIORYTET PF'
            shipping['name'] = 'PRIORYTET FIRMOWA'
            shipping['price_before_discount'] = bs_order['delivery_price']
            shipping['price'] = float(bs_order['delivery_price'])
            shipping['qty'] = 1
            products.append(shipping)
        return products
