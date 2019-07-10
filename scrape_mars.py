# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape_info():  
    browser = init_browser()
    
    # create dictionary for scraped data
    mars_data = {}
 
    #NASA Mars News
    url_news = 'https://mars.nasa.gov/news'
    browser.visit(url_news)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    #JPL Mars Space Images - Featured Image
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'
    
    mars_data["featured_image_url"] = featured_image_url 

    #Mars Weather
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize").text
    
    mars_data["mars_weather"] = mars_weather
    
    #Mars Facts
    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)
    df = tables[0]
    df.columns = ['Description','Value']
    df.set_index('Description', inplace=True)
    # mars_facts = df.to_html('table.html',index=False)
    mars_facts = df.to_html()
    
    mars_data["mars_facts"] = mars_facts
    
    #Mars Hemispheres
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    domain_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

    for i in items:
        title = i.find('h3').text
        page_url = i.find('a', class_="itemLink product-item")['href']
        browser.visit(domain_url + page_url)
        page_html = browser.html
        soup = bs(page_html, 'html.parser')
        img_url = domain_url + soup.find('img', class_="wide-image")['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
            
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_data
