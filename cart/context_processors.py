# context processor is a python function that takes request object and returns a dictionary that gets added to the request context
# it allows to have context variables available to all templates at the same time
from .cart import Cart


def cart_context(request):  # this function name is used only in the settings of the project in the TEMPLATES
    return {'cart': Cart(request)}