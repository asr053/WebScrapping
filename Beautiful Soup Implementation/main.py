import requests
from bs4 import BeautifulSoup
import csv
import os

# code to extract the data from api
def fetch_and_extract_data(api_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data_list = []

        articles = soup.find_all('article', class_='blog-item')
        if(not articles):
            check = False
            return data_list
        for article in articles:
            h6_tag = article.find('h6')
            title = h6_tag.find('a').get_text(strip=True) if h6_tag and h6_tag.find('a') else ''

            date_tag = article.find('div', class_='bd-item').find('span')
            date = date_tag.get_text(strip=True) if date_tag else ''

            img_tag = article.find('div', class_='img')
            image_url = img_tag.find('a')['data-bg'] if img_tag and img_tag.find('a') and 'data-bg' in img_tag.find('a').attrs else ''

            likes_tag = article.find('a', class_='zilla-likes')
            likes_count = likes_tag.find('span').get_text(strip=True) if likes_tag else '0 likes'

            data_list.append({
                'Title': title,
                'Date': date,
                'Image URL': image_url,
                'Likes Count': likes_count
            })

        return data_list
    else:
        print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
        return None

# code to write the data_list into csv_file
def write_to_csv(data_list, csv_file):
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        if csvfile.tell() == 0:
            csv_writer.writerow(['Title', 'Date', 'Image URL', 'Likes Count'])

        for data_row in data_list:
            csv_writer.writerow([data_row['Title'], data_row['Date'], data_row['Image URL'], data_row['Likes Count']])

def _csv(csv_file):
    file_exists = os.path.exists(csv_file)

    with open(csv_file, 'a+', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        if file_exists:
            csvfile.truncate(0)
            csvfile.seek(0)
        
        if not file_exists or csvfile.tell() == 0:
            csv_writer.writerow(['Title', 'Date', 'Image URL', 'Likes Count'])

        

base_url = 'https://rategain.com/blog/'
csv_file = 'output_data.csv'
num_pages = 45
page_num = 2
check = True

_csv(csv_file)
api_url_first_page = base_url
data_list_first_page = fetch_and_extract_data(api_url_first_page)

if data_list_first_page:
    write_to_csv(data_list_first_page, csv_file)
    print(f"Data from the first page has been successfully written to {csv_file}")

while check :
    api_url = f'{base_url}page/{page_num}/'
    page_num += 1
    data_list = fetch_and_extract_data(api_url)

    if data_list:
        write_to_csv(data_list, csv_file)
        print(f"Data from page {page_num} has been successfully written to {csv_file}")
