from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape(driver):
    pageInfo = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'newly-added-items__item__image')
            )
        )
    except Exception as e:
        print(e)
        driver.quit()

    searchResults = driver.find_elements_by_class_name("newly-added-items__item")

    for result in searchResults:
        element = result.find_element_by_css_selector('a')
        link = element.get_attribute('href')
        print('\n' + link)

        header = result.find_element_by_class_name('newly-added-items__item__name').text
        print(header)

        try:
            price = result.find_element_by_class_name('newly-added-items__item__price').text
            print(price)
        except Exception as e:
            print('Class not found')
            price = 'No price set.'

        pageInfo.append({
            'header': header, 'link': link, 'price': price, 'status': ''
        })

    return pageInfo

path = "/chrome/chromedriver.exe" # Path to chromedriver
url = 'https://www.amiami.com/eng/search/list/?s_st_condition_flg=1&s_sortkey=preowned'
# keyword = 'stocks'

# driver = webdriver.Chrome(path)
options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(url)

# SEARCH: Look for search bar with name 'q' and input keyword
# searchBar = driver.find_element_by_name('q')
# searchBar.send_keys(keyword)
# searchBar.send_keys('\n')

# Scraper
scrape(driver)

# List to save results
infoAll = []
infoAll.extend(scrape(driver))

df = pd.DataFrame(infoAll)
fileName = 'buyfag_test.csv'

db_df = pd.read_csv('buyfag_test.csv', index_col=0, header=0)
df = df.append(db_df)
df.to_csv(fileName)

driver.quit()