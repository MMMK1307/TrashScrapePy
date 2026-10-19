import requests
import bs4
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def main():
    driver = webdriver.Chrome()
    driver.get("https://scrapingsandbox.com/infinite-scroll")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(response.text, "html.parser")
    d = input()


if __name__ == "__main__":
    main()
