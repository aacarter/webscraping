from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)

#def init_browser(): 
    #executable_path = {"executable_path": "chromedriver.exe"}
    #return Browser("chrome", **executable_path, headless=False)


def scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find_all('div', class_="content_title")[0]
    news_title = news.text.strip()
    news_paragraph = soup.find_all('div', class_="rollover_description_inner")[0]

    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    image_link = 'https://www.jpl.nasa.gov'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_present_by_text('more info', wait_time=5)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.body.find_all('figure', class_='lede')
    for result in results:  
        img = result.find('a')
    img_url = img['href']
    featured_image_url = image_link + img_url
    url3='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_tweet = soup.find_all('p', class_="TweetTextSize")[0]
    mars_weather = mars_tweet.text.strip()
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    mars_df = tables[0]
    mars_df.rename(columns={1:'Values', 0:'Facts'}).set_index('Facts')

    return news_title
    return news_p
    return featured_image_url
    return mars_weather
    return tables