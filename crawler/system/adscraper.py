import io
import os
import csv
import time
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from django.core.files import File
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from icecream import ic


def is_empty_image(image):
    """
    Function to check if an image is empty.
    """
    grayscale_image = image.convert('L')
    pixels = np.array(grayscale_image)
    intensity_mean = np.mean(pixels)
    threshold = 10
    return intensity_mean < threshold


def get_last_screenshot_count(file_paths):
    last_screenshot_count = -1
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        try:
            screenshot_count = int(file_name.split("_")[-1].split(".")[0])
            if screenshot_count > last_screenshot_count:
                last_screenshot_count = screenshot_count
        except ValueError:
            continue
    return last_screenshot_count


def scrape_google_ads(query, max_ads=4):
    """
    function to scrape google ads from google search results.

    Args:
        query (str): query to search for
    """

    os.makedirs(f"media/data/{query}", exist_ok=True)
    if os.path.exists(f"media/data/{query}"):
        pass
    else:
        os.makedirs(f"media/data/{query}", exist_ok=True)

    os.makedirs(f"media/data/{query}/full", exist_ok=True)
    if os.path.exists(f"media/data/{query}/full"):
        pass
    else:
        os.makedirs(f"media/data/{query}/full", exist_ok=True)

    # Set up selenium webdriver
    CHROMEDRIVER_PATH = '/home/nobinkhan/Downloads/chromedriver/chromedriver'
    WINDOW_SIZE = "2048,1080"
    chrome_service = Service(CHROMEDRIVER_PATH)

    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    scraper = webdriver.Chrome(service=chrome_service, options=chrome_options)

    url = f"https://www.google.com/search?q={query}"
    scraper.get(url)
    time.sleep(2)

    soup = BeautifulSoup(scraper.page_source, "html.parser")

    scrapped_data = []
    target_divs = soup.find_all('div', class_='uEierd')
    for div in target_divs:
        title = div.find('div', class_='QfkTvb', role='heading').find('span').text.strip().replace('\n', '').replace('\t', '')
        description = div.find('div', class_='Va3FIb r025kc lVm3ye').get_text().strip().replace('\n', ' ').replace('\xa0', ' ').replace('<em class="TNT2l AStapd">Ads</em>', 'Ads ').replace('\t', '').replace('<em class="TNT2l AStapd">Ad</em>', 'Ad ')
        link = div.find('div', class_='v5yQqb').find('a')['href']
        scrapped_data.append({
            'ad_url': link, 
            'ad_title':title, 
            'ad_description': description, 
            'query': query, 
            'company_contact_number':"Not Found", 
            'company_board_members':"Not Found", 
            'company_email':"Not Found", 
            'company_board_member_role':"Not Found", 
            'whois':"Not Found"
        })

    # saving full image screenshot
    scraper.save_screenshot(f"media/data/{query}/full/full_page.png")
    initial_ads = scraper.find_elements(By.CSS_SELECTOR, ".uEierd")

    # saving individual ads image
    for loop_index, web_element in enumerate(initial_ads):

        location = web_element.location
        size = web_element.size
        full_image = Image.open(f"media/data/{query}/full/full_page.png")
        left = location["x"]
        top = location["y"]
        right = location["x"] + size["width"]
        bottom = location["y"] + size["height"]

        full_image = full_image.crop((left, top, right, bottom))

        #last screenshot
        last_screenshot_count = get_last_screenshot_count(
            file_paths=os.listdir(f"media/data/{query}/")
        )
        if not is_empty_image(full_image):
            ic(full_image.info)
            full_image.save(f"media/data/{query}/{query}_{last_screenshot_count+1}.png")
            buffer = io.BytesIO()
            full_image.save(buffer, format='png')  # Maintain original format
            buffered_file = File(buffer, f"{query}_{last_screenshot_count+1}.png")
            scrapped_data[loop_index].update(screenshot=buffered_file)
    return scrapped_data


def geotagging(query):
    url = f"https://www.google.com/search?q={query}"
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--disable-gpu")
    service = Service("path/to/chromedriver")
    scraper = webdriver.Chrome(service=service, options=option)
    
    scraper.set_window_size(2048, 1080)
    scraper.get(url)
    time.sleep(2)
    query_list_geo = []
    try:
        scraper.find_element(By.CLASS_NAME, "HzHK1").click()
        time.sleep(2)
        if scraper.find_element(By.CLASS_NAME, "QjCHvc").text.strip() == "No results found":
            return []
        first_geo = scraper.find_elements(By.CLASS_NAME, "QjCHvc")
        for i, geo in enumerate(first_geo):
            if i >= 4:
                break
            q = geo.find_element(By.TAG_NAME, "a").get_attribute("data-query")
            query_list_geo.append(q)
        return query_list_geo
    except Exception:
        return [query]


def save_ads_to_csv(ads):
    """
    Function to save ads to a CSV file.

    Args:
        ads (list): List of ads to save
    """

    header = ["query", "title", "url", "description", "contact_number", "company_board_members","company_email", "whois", "company_board_members_role", "secondary Contact","screenshot"]

    if not os.path.exists("ads.csv"):
        with open("ads.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    existing_data = []

    with open("ads.csv", "r") as f:
        reader = csv.DictReader(f)
        existing_data = [(row.get('url', ''),row.get('title','')) for row in reader]

    new_ads = []

    for ad in ads:
        if existing_data == []:
            new_ads.append(ad)
        else:
            if ad['url'] not in [data[0] for data in existing_data] and ad['title'] not in [data[1] for data in existing_data]:
                new_ads.append(ad)

    if new_ads:
        with open("ads.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerows(new_ads)
