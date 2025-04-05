from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def crawl_gold_data():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(), options=options)

    url = "https://giavang.org/"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table')
    driver.quit()

    data = []
    if table:
        rows = table.find_all('tr')
        current_location = None
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cells = [col.get_text(strip=True) for col in cols]
            if cells and cells[0] == 'Khu vực':
                continue
            if len(cells) == 4:
                current_location = cells[0]
                item = {
                    'location': cells[0],
                    'brand': cells[1],
                    'buy': cells[2],
                    'sell': cells[3],
                }
            elif len(cells) == 3:
                item = {
                    'location': current_location,
                    'brand': cells[0],
                    'buy': cells[1],
                    'sell': cells[2],
                }
            else:
                continue
            data.append(item)
    return data
