from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    rating: float
    sku: str
    vendor: str
    category: str
    in_stock: bool
    link: str
