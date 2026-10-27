import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import bs4

from models import Product


class Scrapper:
    max_products: int
    options: Options

    def __init__(self, debug: bool=False, max_products: int=100):
        self.options = Options()
        if not debug:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        self.max_products = max_products

    @staticmethod
    def try_find_element(driver: webdriver.Chrome, by: ByType = By.ID, value: str = ""):
        try:
            return driver.find_element(by, value)
        except NoSuchElementException:
            return None

    def get_all_products(self):
        driver = webdriver.Chrome(self.options)
        driver.get("https://scrapingsandbox.com/infinite-scroll")
        self.load_all_products(driver)
        products = self.extract_products(driver)
        driver.close()
        return products

    def load_all_products(self, driver: webdriver.Chrome):
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            end_text = self.try_find_element(driver, By.CSS_SELECTOR, ".text-sm.font-mono")
            if end_text and "Loading" not in end_text.text:
                print("Ended")
                return
            product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            print(len(product_elements))
            if len(product_elements) >= self.max_products:
                return

    def extract_products(self, driver: webdriver.Chrome) -> list[Product]:
        main_container = driver.find_element(By.CSS_SELECTOR, "main")
        main_html = main_container.get_attribute("innerHTML")
        main_soup = bs4.BeautifulSoup(main_html, "html.parser")
        products: list[Product] = []
        for product_soup in main_soup.find_all(class_="product-card"):
            product = self.parse_single_product(product_soup)
            products.append(product)
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

    @staticmethod
    def parse_single_product_alt(product_soup: bs4.Tag, link: str):
        price = product_soup.select_one("div.flex.items-baseline.gap-3 > span.text-3xl.font-bold.font-mono.text-primary").text
        name = product_soup.select_one("div:nth-child(1) > h1").text
        rating = product_soup.select_one("div:nth-child(1) > div.flex.items-center.gap-3.mt-3 > div > span.text-sm.font-mono.font-semibold.text-foreground").text
        product = Product(
            name,
            float(price.replace("$", "")),
            float(rating),
            product_soup.select_one("div.grid.grid-cols-2.gap-3 > div:nth-child(1) > span").text,
            product_soup.select_one("div:nth-child(1) > div.flex.items-center.gap-2.mb-2 > span.text-xs.font-mono.uppercase.tracking-wider.text-muted-foreground").text,
            product_soup.select_one("div:nth-child(1) > div.flex.items-center.gap-2.mb-2 > span.inline-flex.items-center.justify-center.rounded-full.border.border-transparent.text-secondary-foreground.font-mono").text,
            "in stock" in product_soup.select_one("div.space-y-6 > div:nth-child(1) > div.flex.items-center.gap-3.mt-3 > span").text.lower(),
            link
        )
        return product

    def get_all_products_alt(self):
        products: [Product] = []
        for i in range(1, 501):
            path = f"/product/{i}"
            response = requests.get(f"https://scrapingsandbox.com{path}")
            if not response.ok:
                continue
            product_html = response.text
            main_soup = bs4.BeautifulSoup(product_html, "html.parser")
            product_soup = main_soup.select("body > div.min-h-screen.bg-background > main > div > div.space-y-6")
            products.append(self.parse_single_product_alt(product_soup[0], path))

            if len(products) >= self.max_products:
                break

        return products
