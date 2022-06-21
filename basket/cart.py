from catalogue.models import Product, Discount

CART = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART)
        if not cart:
            cart = self.session[CART] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            try:
                remind = item['product'].count - item['product'].purchase_count
                if item['quantity'] > remind:
                    item['quantity'] = remind
                yield item
            except:
                del item

    def save(self):
        self.session.modified = True

    def add(self, product, quantity, color=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
            self.cart[product_id]['product_color'] = {}
        if color:
            color_id = str(color.id)
            product_color = self.cart[product_id].get('product_color')
            if not product_color:
                self.cart[product_id]['product_color'] = {}
            if color_id not in self.cart[product_id]['product_color']:
                self.cart[product_id]['product_color'][str(color.id)] = {"color": color, "quantity": 0}
            self.cart[product_id]['product_color'][str(color.id)]['quantity'] += quantity
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def change_quantity(self, product_id, quantity):
        if not 1 < quantity < 10:
            quantity = 1
        self.cart[str(product_id)]['quantity'] = quantity
        self.save()

    def total_price(self):
        total = sum([item['product'].get_price() * item['quantity'] for item in self])
        if self.session.get('discount'):
            discount = Discount.objects.filter(code=self.session['discount']['code'])
            if discount.exists():
                discount = discount.first()
                discount_mount = (total * discount.discount) // 100
                return total - discount_mount
            else:
                del self.session['discount']
                self.save()
        return total

    def remove_item(self, product_id):
        del self.cart[str(product_id)]
        self.save()

    def add_discount_code(self, discount_code):
        self.session['discount'] = {'code': discount_code}
        self.save()
        return True

    def remove(self):
        del self.cart
        self.save()
        return True
