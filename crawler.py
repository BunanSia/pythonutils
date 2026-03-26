import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configuration
START_URL = "https://www.example.com"
STOP_CONDITION = "-anything.html"

# Setup Driver with fixes for "GET FAILED"
chrome_options = Options()
chrome_options.add_argument("--headless") # Runs without opening a window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

visited = set()
queue = [START_URL]

def clean_filename(url):
    return url.replace("https://", "").replace("/", "_").replace(":", "")[:200] + ".txt"

try:
    while queue:
        current_url = queue.pop(0)
        if current_url in visited:
            continue

        try:
            driver.get(current_url)
            time.sleep(0.1) # Prevent being blocked
            visited.add(current_url)
            
            # Stop recursion if the URL reaches the deep nested path
            if STOP_CONDITION in current_url:
                # Save Content
                content = driver.find_element(By.TAG_NAME, "body").text
                with open(clean_filename(current_url), "w", encoding="utf-8") as f:
                    f.write(content)
                continue

            # Find Links
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and "big5" in href:
                    if href not in visited and href not in queue:
                        queue.append(href)
                        
        except Exception as e:
            print(f"Failed to load {current_url}: {e}")

finally:
    driver.quit()
    print("Done.")