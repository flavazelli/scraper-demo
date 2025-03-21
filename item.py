class Item:   
    """
    A class to represent an item with various pricing attributes.
    Attributes:
    ----------
    store_id : str, optional
        The store identifier for the item (default is None).
    brand : str, optional
        The brand of the item (default is None).
    name : str, optional
        The name of the item (default is None).
    size : str, optional
        The size of the item (default is None).
    regular_price : float, optional
        The regular price of the item (default is None).
    sale_price : float, optional
        The sale price of the item (default is None).
    price_per_kg : float, optional
        The price per kilogram of the item (default is None).
    price_per_100ml : float, optional
        The price per 100 milliliters of the item (default is None).
    price_per_100g : float, optional
        The price per 100 grams of the item (default is None).
    price_per_unit : float, optional
        The price per unit of the item (default is None).
    Methods:
    -------
    to_mongo_dict():
        Converts the item attributes to a dictionary suitable for MongoDB storage.
    """
    def __init__(self, store_id=None, brand=None, name=None, size=None, regular_price=None, sale_price=None, price_per_kg=None, price_per_100ml=None, price_per_100g=None, price_per_unit=None):
        self._store_id = store_id
        self._brand = brand
        self._name = name
        self._size = size
        self._regular_price = regular_price
        self._sale_price = sale_price
        self._price_per_kg = price_per_kg
        self._price_per_100ml = price_per_100ml
        self._price_per_100g = price_per_100g
        self._price_per_unit = price_per_unit

    @property
    def store_id(self):
        return self._store_id

    @store_id.setter
    def store_id(self, value):
        self._store_id = value

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def regular_price(self):
        return self._regular_price
    
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @regular_price.setter
    def regular_price(self, value):
        if isinstance(value, str):
            value = float(value)
        self._regular_price = value

    @property
    def sale_price(self):
        return self._sale_price

    @sale_price.setter
    def sale_price(self, value):
        if isinstance(value, str):
            value = float(value)
        self._sale_price = value

    @property
    def price_per_kg(self):
        return self._price_per_kg

    @price_per_kg.setter
    def price_per_kg(self, value):
        if isinstance(value, str):
            value = float(value)
        self._price_per_kg = value

    @property
    def price_per_100ml(self):
        return self._price_per_100ml

    @price_per_100ml.setter
    def price_per_100ml(self, value):
        if isinstance(value, str):
            value = float(value)
        self._price_per_100ml = value

    @property
    def price_per_100g(self):
        return self._price_per_100g

    @price_per_100g.setter
    def price_per_100g(self, value):
        if isinstance(value, str):
            value = float(''.join(c for c in value if c.isdigit() or c == '.'))
        self._price_per_100g = value

    @property
    def price_per_unit(self):
        return self._price_per_unit

    @price_per_unit.setter
    def price_per_unit(self, value):
        if isinstance(value, str):
            value = float(value)
        self._price_per_unit = value

    
    def to_mongo_dict(self):
        mongo_dict = {}
        if self._store_id:
            mongo_dict['store_id'] = self._store_id
        if self._brand:
            mongo_dict['brand'] = self._brand
        if self._name:
            mongo_dict['name'] = self._name
        if self._size:
            mongo_dict['size'] = self._size
        if self._regular_price is not None:
            mongo_dict['regular_price'] = self._regular_price
        if self._sale_price is not None:
            mongo_dict['sale_price'] = self._sale_price
        if self._price_per_kg is not None:
            mongo_dict['price_per_kg'] = self._price_per_kg
        if self._price_per_100ml is not None:
            mongo_dict['price_per_100ml'] = self._price_per_100ml
        if self._price_per_100g is not None:
            mongo_dict['price_per_100g'] = self._price_per_100g
        if self._price_per_unit is not None:
            mongo_dict['price_per_unit'] = self._price_per_unit
        return mongo_dict