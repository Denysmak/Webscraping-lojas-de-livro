from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time


def get_html(page, asin):
    url = f'https://www.amazon.com.br/{asin}'
    page.goto(url)
    time.sleep(5)
    html = HTMLParser(page.content())
    return html

def parse_html(html, asin):
    print(html.css_first('title').text())
    print(asin)
'''
def run():
    asin = 'B09VNBCFDJ'
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    html = get_html(page, asin)
    parse_html(html, asin)
'''
def run():
    asin = 'B09VNBCFDJ'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        html = get_html(page, asin)
        parse_html(html, asin)

def main():
    run()


main()