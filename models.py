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


@dataclass
class ProductCounting:
    total: int
    lowest_price: Product  | None
    highest_price: Product | None
    avg_price: float
    best_ratted: Product | None

    @staticmethod
    def perform_count(products: list[Product]):
        l_price = None
        h_price = None
        b_ratted = None
        total_price = 0

        for product in products:
            total_price += product.price

            if l_price is None or product.price < l_price.price:
                l_price = product

            if h_price is None or product.price > h_price.price:
                h_price = product

            if b_ratted is None or product.rating > b_ratted.rating:
                b_ratted = product

        if len(products) == 0:
            avg_price = 0
        else:
            avg_price = round(total_price / len(products), 2)

        return ProductCounting(
            len(products),
            l_price,
            h_price,
            avg_price,
            b_ratted,
        )