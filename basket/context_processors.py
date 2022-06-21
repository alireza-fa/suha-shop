from .cart import Cart


def cart(request):
    basket = Cart(request)
    return {"cart": basket}
