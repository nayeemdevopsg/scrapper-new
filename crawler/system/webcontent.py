import time
from django.db.models import Q
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from crawler.system.adscraper import scrape_google_ads
from crawler.models import Ad_model
from crawler.serializer import Ad_modelSerializer

def whois_lookup (url):
    print("started whois lookup crawling...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service("/usr/local/bin/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)
    try:
        url = "https://www.whois.com/whois/" + url
        scraper.get(url)
        time.sleep(4)
        try:
            boards = scraper.find_elements(By.CLASS_NAME, "df-value")
            board_members = []
            for board in boards:
                try:
                    board_members.append(board.text)
                except Exception:
                    pass
            return board_members[5]
        except Exception:
            return ""
    except Exception:
        return ""
    
def facebook_crawler(url):
    print("started facebook crawling...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service("/usr/local/bin/chromedriver")
    scraper = webdriver.Chrome(service=service, options=options)
    scraper.set_window_size(2048, 1080)
    try:
        url = "https://www.google.com/search?q=" + "facebook page "+ url
        scraper.get(url)
        scraper.find_element(By.CLASS_NAME, "yuRUbf").click()
        time.sleep(2)
        scraper.find_element(By.CLASS_NAME,"x1i10hfl.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1").click()
        time.sleep(2)
        contact_number = scraper.find_elements(By.CLASS_NAME, "x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x41vudc.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h")
        contact_list = []
        for contact in contact_number:
            try:
                contact_list.append(contact.text)
            except Exception:
                contact_list.append("")
        return contact_list
    except Exception:
        return ""

def url_content_scraper(queries):
    return_value = []
    for query in queries:
        data_list: list = scrape_google_ads(query)
        for data in data_list:
            existing_ad = Ad_model.objects.filter(Q(ad_url=data.get('ad_url')) | Q(ad_title=data.get('ad_title')))
            if not existing_ad:
                return_value.append(data)
    serializer = Ad_modelSerializer(data=return_value, many=True)
    if serializer.is_valid():
        serializer.save()
        return len(serializer.data)
    return 0

