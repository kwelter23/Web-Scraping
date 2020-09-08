from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "c:/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    #News Title
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    news_section = soup.find('div', id='page')
    news_title = news_section.find('h3').text

    # News Paragraph
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    # Print one paragraph texts
    paragraph = soup.find('div', class_='article_teaser_body').text

    #Featured Image

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    element = browser.find_by_id('full_image')
    details = element['data-link']
    image_url = "https://www.jpl.nasa.gov" + details
    browser.visit(image_url)
    featured_element = browser.find_by_tag('figure')
    featured_element_sub = featured_element.find_by_tag('a')
    featured_image_url = featured_element_sub['href']

    #Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    #tables[0].head()
    df = tables[0]
    df.columns = [' ', 'Mars']
    df.set_index(' ', inplace=True)
    df.head(10)

    #Mars facts to html table
    html_table = df.to_html()
    html_table.replace('\n', '')

    #Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    #Create Dicttionary
    hemisphere_image_urls = []
    img_url = {}
    title = {}

    # Find titles and image urls
    element = soup.find('div', class_="collapsible results")
    element_sub = element.findAll(class_="item")

    for item in element_sub:
        title_section = item.find('div', class_="description")
        title_sub_section = title_section.find('a', class_='itemLink product-item')
        title = title_sub_section.find('h3')
        
        image_section = item.find('a', class_="itemLink product-item")
        image_page = image_section['href']
        image_link = "https://astrogeology.usgs.gov" + image_page
        browser.visit(image_link)
        
        html = browser.html
        soup = bs(html, "html.parser")
        image_page_section = soup.find('div', id='wide-image')
        image_page_sub_section = image_page_section.find('img', class_='wide-image')
        img_link = image_page_sub_section['src']
        img_url = "https://astrogeology.usgs.gov" + img_link
        hemisphere = {"title": title.text, "img_url": img_url}
        hemisphere_image_urls.append(hemisphere)

    mars = {'NewsTitle':news_title, 'FeaturedImageURL':featured_image_url, 'Paragraph':paragraph, 'HTMLTable':html_table, 'Hemispheres':hemisphere_image_urls}

    return mars