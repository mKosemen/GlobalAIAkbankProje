
class Pizzas:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class VeganPizzas(Pizzas):
    type = "Vegan"

class MangalPizzas(Pizzas):
    type = "Mangal"

class DenizdenPizzas(Pizzas):
    type = "Denizden"

class Sauces:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class Orders:
    def __init__(self, customerName, pizza, size, sauces, price, date):
        self.customerName = customerName
        self.pizza = pizza
        self.size = size
        self.sauces = sauces
        self.price = price
        self.date = date
