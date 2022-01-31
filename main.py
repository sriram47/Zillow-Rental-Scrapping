import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_driver_path = "/Users/sriramramachandran/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.61529005957031%2C%22east%22%3A-122.25136794042969%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
# Write your code below this line 👇
response = requests.get(URL, headers= headers)
webpage_content = response.text

soup = BeautifulSoup(webpage_content, "html.parser")
listing_address = soup.select(".list-card-top a")
# print(listing_address)
all_links = []
for items in listing_address:
    url = items["href"]
    all_links.append(url)

list_price_elements = soup.select(".list-card-heading")
all_prices = []
for price in list_price_elements:
    try:
        list_price = price.select(".list-card-price")[0].contents[0]
    except IndexError:
        try:
            list_price = price.select(".list-card-details li")[0].contents[0]
        except IndexError:
            pass
    finally:
        all_prices.append(list_price)


list_address_elements = soup.select(".list-card-info address")
all_addresses = [address.getText().split(" | ")[-1] for address in list_address_elements]
print(all_addresses)
# https://forms.gle/akwnQoxfM8GGm51v8

for n in range(len(all_links)):
    driver.get("https://forms.gle/akwnQoxfM8GGm51v8")
    time.sleep(2)
    address_question = driver.find_element_by_xpath(
        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price_question = driver.find_element_by_xpath(
        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link_question = driver.find_element_by_xpath(
        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit_button = driver.find_element_by_xpath(
        "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")

    address_question.send_keys(all_addresses[n])
    price_question.send_keys(all_prices[n])
    link_question.send_keys(all_links[n])
    submit_button.click()

# for n in range(len(all_links)):






