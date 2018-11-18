from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import sys
import time

sys.setrecursionlimit(10000)
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'    
    response = requests.get(url)
    mars_dict={}
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find_all('div', class_="content_title")[0]
    news_title = news.text.strip()
    news_paragraph = soup.find_all('div', class_="rollover_description_inner")[0]
    news_p = news_paragraph.text.strip()
    mars_dict['news_title']=news_title
    mars_dict['news_paragraph']=news_p
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
    mars_dict['featured_image_url'] = featured_image_url
    url3='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_tweet = soup.find_all('p', class_="TweetTextSize")[0]
    mars_weather = mars_tweet.text.strip()
    mars_dict['mars_weather'] = mars_weather
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    mars_df = tables[0]
    mars_df.rename(columns={1:'Values', 0:'Facts'}).set_index('Facts')
    mars_df_html = mars_df.to_html(index=False).replace('\n', "")
    mars_dict['mars_html'] = mars_dict
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url5='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    homepage = 'https://astrogeology.usgs.gov'
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    astropedia = soup.find_all('div',class_='description')
    astro_list = []
    for a in astropedia:
        title = homepage+a.find('a')['href']
        astro_list.append(title)
    mars_list = []
    for astro in astro_list:
        browser.visit(astro)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        astro_dict = {}
        image = soup.find('img', class_ = 'wide-image')
        title = soup.find('h2')
        img = image['src']
        title_url = title.text
        img_url = homepage+img
        astro_dict['image_url'] = img_url
        astro_dict['title'] = title_url
        mars_list.append(astro_dict)
        time.sleep(3)
    mars_dict['mars_list'] = mars_list
    # mars_dict['cerberus'] = mars_list[0]
    # mars_dict['schiaparelli'] = mars_list[1]
    # mars_dict['syrtis_major'] = mars_list[2]
    # mars_dict['valles_marineris'] = mars_list[3]
    browser.quit()
    return mars_dict
