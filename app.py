
from flask import Flask, render_template, request

app = Flask("TrashScrapePy")


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
    data = {
        "category": request.args.get("category")
    }
    return render_template("product_list.html", **data)

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
