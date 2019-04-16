from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

#initalizing the browser connection
def init_browser():
    executable_path = {"executable_path": "C:/Users/gairo/Downloads/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,"html.parser")
    result=soup.find('div',class_='list_text')
    news_title=result.find('div',class_='content_title').a.get_text()
    news_para=result.find('div',class_='article_teaser_body').get_text()
    
 
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(url)
    # time.sleep(1)
    base_url=url.split('/spaceimages')[0]

    browser.is_element_present_by_id('full_image')
    browser.click_link_by_id('full_image')
    browser.is_element_present_by_text('more info')
    browser.click_link_by_partial_text('more info')
    html=browser.html
    soup=bs(html,"lxml")
    image_=soup.find('figure',class_='lede').a['href']
    image_=soup.find('figure',class_='lede').a['href']
    featured_image_url=base_url+image_
    
    
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'lxml')
    mars_weather=soup.find('div',class_='js-tweet-text-container').p.get_text()

    url='https://space-facts.com/mars/'
    tables=pd.read_html(url)
    df=tables[0]
    df.columns=["description","values"]
    html_table_string=df.to_html(index=False)
    html_table_string=html_table_string.replace('\n',"")

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'lxml')
    mars_url_first_part=url.split('/search')[0]
    hemisphere_image_urls=[]
    results=soup.find_all('a',class_='itemLink product-item')
    for x in range(0,len(results),2):
        try:
            mars_item_url=results[x]['href']
        
            mars_url=mars_url_first_part + mars_item_url
            browser.visit(mars_url)
            
            mars_html=browser.html
            mars_soup=bs(mars_html,'lxml')
            mars_title=mars_soup.find('section',class_='block metadata').find('h2',class_='title').get_text()
            get_url=browser.find_link_by_text("Sample").first
            mars_url=get_url['href']
            
            if mars_url and mars_title:
                print("=================")
                print(mars_url)
                print(mars_title)
                
                hemisphere_image_url = {
                    'title':mars_title,
                    'img_url':mars_url,
                }
                hemisphere_image_urls.append(hemisphere_image_url)
            
        except Exception as e:
                pass

    mars_scraped_info={
            "news_title":news_title,
            "news_para":news_para,
            "featured_image_url":featured_image_url,
            "mars_weather":mars_weather,
            "html_table_string":html_table_string,
            "hemisphere_image_urls":hemisphere_image_urls
    }

    browser.quit()
    return mars_scraped_info
    
if __name__=="__main__":
   mars_scraped_info= scrape()
   print(mars_scraped_info)
