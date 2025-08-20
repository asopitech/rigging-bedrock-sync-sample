import rigging as rg
from typing import List


class Product(rg.Model, tag="product"):
    """A product in the catalog with name, price, and stock status."""
    name: str = rg.element()
    price: float = rg.element()
    in_stock: bool = rg.element()

class Catalog(rg.Model, tag="catalog"):
    """A catalog containing a list of products."""
    products: List[Product]