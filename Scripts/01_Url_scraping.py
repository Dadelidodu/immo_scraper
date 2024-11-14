import random
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# List of User-Agent strings to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
]

# Function to get a random User-Agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")

# Set up Selenium WebDriver using ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# List to hold all the hrefs from each page
all_hrefs = []

# Function to extract links from a given URL
def extract_links(url):
    retry_attempts = 3
    for page_num in range(1, 334):
        for attempt in range(retry_attempts):
            try:
                # Navigate to the page
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-results__item')))
                
                page_source = driver.page_source
                
                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')
                list_items = soup.find_all('li', class_='search-results__item')
                
                # Collect all hrefs on this page
                hrefs = []
                for li in list_items:
                    for a in li.find_all('a', href=True):
                        href = a['href']
                        hrefs.append(href)
                
                all_hrefs.extend(hrefs)
                
                # Print progress
                print(f"Page {page_num} - {len(hrefs)} links extracted.")
                break  # Exit retry loop if successful
                
            except TimeoutException:
                print(f"Attempt {attempt + 1} for page {page_num} timed out.")
                continue

# Main function to loop through each URL and extract links
def main():
    url_list = [
        'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minPrice=0&minSurface=1&isAPublicSale=false&isALifeAnnuitySale=false&isNewlyBuilt=false&page={page_num}&orderBy=relevance',
        'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minPrice=0&minSurface=200&isAPublicSale=false&isALifeAnnuitySale=false&isNewlyBuilt=false&page={page_num}&orderBy=relevance'
    ]
    
    # Extract links from each URL in the list
    for url in url_list:
        extract_links(url)

    # Close the driver after collecting all links
    driver.quit()

    # Export all hrefs to a CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extracted_links_path = os.path.join(script_dir, '../csv_files/extracted_links.csv')
    with open(extracted_links_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Links'])  # Write header
        for href in all_hrefs:
            writer.writerow([href])  # Write each link in a new row

    print("Links have been exported to 'extracted_links.csv'.")

# Run the main function
if __name__ == "__main__":
    main()