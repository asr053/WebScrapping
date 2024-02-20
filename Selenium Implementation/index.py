import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def fetch_and_extract_data(driver, api_url):
    driver.get(api_url)
    data_list = []

    articles = driver.find_elements(By.CSS_SELECTOR, 'article.blog-item')
    for article in articles:
        title = ''
        date = ''
        image_url = ''
        likes_count = '0 likes'

        try:
            h6_tag = article.find_element(By.TAG_NAME, 'h6')
            title = h6_tag.find_element(By.TAG_NAME, 'a').text.strip()
        except NoSuchElementException:
            pass

        try:
            date_tag = article.find_element(By.CSS_SELECTOR, 'div.bd-item span')
            date = date_tag.text.strip()
        except NoSuchElementException:
            pass

        try:
            img_tag = article.find_element(By.CSS_SELECTOR, 'div.img a')
            image_url = img_tag.get_attribute('data-bg').strip() if 'data-bg' in img_tag.get_attribute('outerHTML') else ''
        except NoSuchElementException:
            pass

        try:
            likes_tag = article.find_element(By.CSS_SELECTOR, 'a.zilla-likes span')
            likes_count = likes_tag.text.strip() if likes_tag else '0 likes'
        except NoSuchElementException:
            pass

        data_list.append({
            'Title': title,
            'Date': date,
            'Image URL': image_url,
            'Likes Count': likes_count
        })

    return data_list

options = Options()
options.headless = True
chrome_driver_path = r'C:\Users\Karma-Yog\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

base_url = 'https://rategain.com/blog/'
csv_file = 'result_data.csv'
current_page = 1

csv_exists = os.path.isfile(csv_file)

with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    if not csv_exists:
        csv_writer.writerow(['Title', 'Date', 'Image URL', 'Likes Count'])

while True:
    api_url = f'{base_url}page/{current_page}/'
    data_list = fetch_and_extract_data(driver, api_url)

    if data_list:
        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for data_row in data_list:
                csv_writer.writerow([data_row['Title'], data_row['Date'], data_row['Image URL'], data_row['Likes Count']])
        print(f"Data from page {current_page} has been successfully written to {csv_file}")
        current_page += 1
    else:
        break

driver.quit()
os.startfile(csv_file)
