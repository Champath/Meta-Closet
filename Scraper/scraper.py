import os

import gridfs
import requests
import tldextract
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Configuration & Setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "fashion_store"

def init_mongodb(uri=MONGO_URI, db_name=DB_NAME):
    """Connects to MongoDB and returns the GridFS instance."""
    client = MongoClient(uri)
    db = client[db_name]
    return gridfs.GridFS(db)

# Web Scraping Functions
def fetch_page(url):
    """Fetches the webpage content for the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

def parse_image_url(page_content, amm):
    """Parses the webpage content and extracts the image URL."""
    print(amm)
    soup = BeautifulSoup(page_content, 'html.parser')
    if amm == "Meesho":
        image_div = soup.find('div', class_='ProductDesktopImage__ImageWrapperDesktop-sc-8sgxcr-0 iEMJCd')
    elif amm == "Amazon":
        image_div = soup.find('div', class_='imgTagWrapper')
    elif amm == "Myntra":
        image_div = soup.find('div', class_='image-grid-image')
    else:
        print("Try from Meesho | Amazon | Myntra")
        
    
    if image_div:
        img_tag = image_div.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
        if image_div and 'style' in image_div.attrs:
            style = image_div['style']
            start = style.find('url(&quot;')
            end = style.find('&quot;)', start)
            if start != -1 and end != -1:
                image_url = style[start+len('url(&quot;'):end]
                return image_url
            else:
                print("URL pattern not found")
        else:
            print("Div with style attribute not found")
        return None

# Image Download & Storage Functions
def download_image(image_url):
    """Downloads the image from the given URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")

def store_image(grid_fs, image_data, filename):
    """Stores the image data in MongoDB using GridFS and returns the file ID."""
    return grid_fs.put(image_data, filename=filename)

# Main Scraper Function
def scrape_and_store(url):
    """Scrapes the dress image from the URL and stores it in MongoDB."""
    try:
        # Fetch and parse page
        page_content = fetch_page(url)
        print("Page Found!")
        extracted = tldextract.extract(url)
        image_url = parse_image_url(page_content, extracted.domain.capitalize())
        if image_url:
            print("Image URL found:", image_url)

            # Download the image
            image_data = download_image(image_url)
            
            # Initialize GridFS and store the image
            fs = init_mongodb()
            filename = os.path.basename(image_url.split("?")[0])  # Clean filename if URL contains params
            file_id = store_image(fs, image_data, filename)
            print(f"File downloaded and stored with ID: {file_id} and file name {filename}")
        else:
            print("Failed to locate image URL on the page.")
        return file_id
    except Exception as e:
        print("An error occurred:", e)
        return None

if __name__ == "__main__":
    target_url = "https://www.amazon.in/GoSriKi-Anarkali-Printed-Dupatta-Yellow-GS_XL_Yellow_X-Large/dp/B0DD78S3M2?ref=dlx_15712_dg_dcl_B0DD78S3M2_dt_mese30_7b_pi&pf_rd_r=JNAXXX7HJRG1V2WVT8GR&pf_rd_p=6c8dabbc-1c17-4851-8d45-67af61f7067b"
    try:
        file_id = scrape_and_store(target_url)
        print("Scraping completed successfully!")
    except Exception as e:
        print("Error:", e)
