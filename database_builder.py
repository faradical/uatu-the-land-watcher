# IMPORT DEPENDENCIES
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import json
from pymongo import MongoClient as MC

# CREATE DATABASE CONNECTION
client = MC()
# import pymongo
# client = pymongo.MongoClient("mongodb://uatu:#watch!@uatu-cluster-shard-00-00.c4ylx.mongodb.net:27017,uatu-cluster-shard-00-01.c4ylx.mongodb.net:27017,uatu-cluster-shard-00-02.c4ylx.mongodb.net:27017/real_estate?ssl=true&replicaSet=atlas-10fsbj-shard-0&authSource=admin&retryWrites=true&w=majority")

DB = client.real_estate

# STATES TO SCRAPE
states = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming'
]

# CREATE WEB DRIVER OBJECT
driver = webdriver.Firefox()

# BEGIN SCRAPING
for state in states:
    #Initialize listings list
    listings = []

    # Iterate over desired number of pages
    for page_num in range(1,5):
        
        # Build URL
        url = f"https://www.landwatch.com/{state}-land-for-sale/price-under-100000/acres-over-1/sort-price-low-high/page-{page_num}"
        
        # Visit Page
        driver.get(url)
        
        # Create soup object to simply search
        body = driver.find_element_by_tag_name("body")
        body_html = body.get_attribute("innerHTML")
        soup = BS(body_html)
        
        # Get listing elements
        li_elems = soup.find_all("div", class_="d99b8 _7c2d9")
        for li in li_elems:
            
            # Get address info from script tag
            script_dict = json.loads(li.find("script").text)
            # Address info
            address = script_dict['address']['streetAddress']
            city = script_dict['address']['addressLocality']
            zipcode = script_dict['address']['postalCode']
            
            # Get the link URL
            link = "https://www.landwatch.com" + li.a['href']
            
            # Retrieve the price
            price_str = li.find("div", class_="b04f6").text
            
            # Retrieve the acreage
            size_str = li.span.text.split(" acres")[0]
            
            # Getting the acreage and price can be a little finicky at times. 
            # Since I am only interested in listing where I can successfully retrieve these, 
            # the rest of the code is in a try/except statement.
            try:
                # Correct price formatting
                price = int(price_str.replace("$","").replace(",",""))

                # Correct size formatting
                size = float(size_str.replace(",",""))

                # Append data to listings
                listing = {
                    "address": address,
                    "city": city,
                    "state": state,
                    "zipcode": zipcode,
                    "price": price,
                    "size": size,
                    "price/acre": price/size,
                    "link": link
                }
                listings.append(listing)

            except:
                pass

    DB[state].insert_many(listings)
    print(f'Retrieved {len(listings)} for {state}.')

# SHUTDOWN THE DRIVER
driver.quit()