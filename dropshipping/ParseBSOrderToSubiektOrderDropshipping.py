from subiekt.ParseBsOrderToSubiektOrder import ParseBsOrderToSubiektOrder

class ParseBSOrderToSubiektOrderDropshipping(ParseBsOrderToSubiektOrder):

    def __init__(self, price):
        ParseBsOrderToSubiektOrder.__init__(self)
        self.price = str(price)

    def parse_products_data(self, bs_order):
        products = []
        product = {}
        product['code'] = '004310'
        product['price'] = self.price
        product['price_before_discount'] = self.price
        product['name'] = 'pośrednictwo sprzedaży'
        product['qty'] = '1'
        products.append(product)
        return products