from flask import Flask, render_template, request

from models import Product, ProductCounting
from scrapper import Scrapper

app = Flask("TrashScrapePy")
products: list[Product]


@app.route("/", methods=["GET"])
def index():
    data = {
        'categories': ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books',
        'Toys', 'Beauty', 'Automotive', 'Health', 'Food & Beverage',
        'Jewelry', 'Office Supplies', 'Pet Supplies', 'Music', 'Art']
    }
    return render_template("index.html", **data)


@app.route("/load-products", methods=["GET"])
def get_products():
    category = request.args.get("category")

    if category:
        filtered_products = [product for product in products if product.category == category]
    else:
        filtered_products = products

    data = {
        "category": category,
        "products": filtered_products,
        "count": ProductCounting.perform_count(filtered_products),
    }

    return render_template("product_list.html", **data)


def main():
    app.run(debug=True, port=8000)


scrapper = Scrapper(
    # debug=True,
    max_products=100,
)
products = scrapper.get_all_products()
# products = scrapper.get_all_products_alt()


if __name__ == "__main__":
    main()

