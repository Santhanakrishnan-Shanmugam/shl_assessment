from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Open the catalog
catalog_url = "https://www.shl.com/solutions/products/product-catalog/"
driver.get(catalog_url)
time.sleep(8)

# Scroll to load all content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Step 1: Collect all hrefs first
links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/products/"]')
urls = []
for link in links:
    url = link.get_attribute("href")
    if url and url not in urls:
        urls.append(url)

print(f"Collected {len(urls)} URLs")

# Step 2: Visit each URL to enrich data
data = []

for url in urls:
    enriched_name = ""
    description = ""
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # Use <h1> as name if available
        try:
            enriched_name = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            enriched_name = ""
        
        # Grab short description
        try:
            description = driver.find_element(By.TAG_NAME, "main").text.replace("\n", " ")[:300]
        except:
            description = ""
    
    except:
        pass
    
    data.append({
        "name": enriched_name,
        "url": url,
        "description": description
    })

driver.quit()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("shl_product_links_enriched.csv", index=False, encoding="utf-8")

print(f"CSV saved with {len(df)} rows")
print(df.head())
