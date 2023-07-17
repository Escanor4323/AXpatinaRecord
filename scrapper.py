from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import time
from urllib.parse import urljoin, urlparse

def download_all_images(url):
    # Configure ChromeDriver and open the webpage
    driver = webdriver.Chrome()
    driver.get(url)

    # Scroll down to the bottom of the page
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # close the browser

    # Create a directory with the name based on the URL's suffix
    folder_name = urlparse(url).path.strip("/").replace("/", "_")
    folder_location = f'./images/{folder_name}'
    os.makedirs(folder_location, exist_ok=True)

    # Continue as before
    img_tags = soup.find_all("img")
    for img in img_tags:
        try:
            img_url = img.attrs.get("src")
            if img_url == "" or img_url is None:
                continue
            img_url = urljoin(url, img_url)
            filename = os.path.join(folder_location, img_url.split("/")[-1])
            img_data = requests.get(img_url).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    urls = ["https://angelamiastudios.com/INDOOR-SCULPTURE",
            "https://angelamiastudios.com/OUTDOOR-SCULPTURE",
            "https://angelamiastudios.com/MINIS",
            "https://angelamiastudios.com/NEW-WORKS",
            "https://angelamiastudios.com/PUBLIC-CORPORATE-SCULPTURE"]
    for url in urls:
        download_all_images(url)
