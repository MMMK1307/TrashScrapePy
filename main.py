import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import bs4

from models import Product


class Scrapper:
    driver: webdriver.Chrome

    def __init__(self, debug=False):
        options = Options()
        if not debug:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options)
        self.driver.get("https://scrapingsandbox.com/infinite-scroll")

    def try_find_element(self, by: By = By.ID, value: str = ""):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None

    def get_all_products(self):
        self.load_all_products()
        self.extract_products()
        return

    def load_all_products(self):
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            end_text = self.try_find_element(By.CSS_SELECTOR, ".text-sm.font-mono")
            if end_text and "Loading" not in end_text.text:
                print("Ended")
                return
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card")
            print(len(product_elements))
            if len(product_elements) >= 100:
                return

    def extract_products(self) -> list[Product]:
        main_container = self.driver.find_element(By.CSS_SELECTOR, "main")
        main_html = main_container.get_attribute("innerHTML")
        main_soup = bs4.BeautifulSoup(main_html, "html.parser")
        products = []
        for product_soup in main_soup.find_all(class_="product-card"):
            product = self.parse_single_product(product_soup)
            products.append(product)
        print(products)
        return products

    @staticmethod
    def parse_single_product(product_soup: bs4.Tag):
        link = product_soup.attrs.get('href')
        vendor = product_soup.find(class_="vendor").text
        rating = product_soup.find(class_="rating").text
        product_name = product_soup.find(class_="product-name").text
        price = product_soup.find(class_="price").text
        category = product_soup.find(class_="category").text
        sku = product_soup.find(class_="sku").text
        availability = product_soup.find(class_="availability").text
        product = Product(
            product_name,
            float(price.replace("$", "")),
            float(rating),
            sku,
            vendor,
            category,
            availability.lower() == "in stock",
            link
        )
        return product

    def close(self):
        self.driver.close()


def main():
    scrapper = Scrapper(
        # True
    )
    scrapper.get_all_products()
    # scrapper.close()


if __name__ == "__main__":
    main()
