import random
import os
import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from extract_functions import extract_locality, extract_zipcode, extract_property_type, extract_property_subtype, extract_price, extract_sale_type, extract_numbers_of_rooms, extract_living_area, extract_equiped_kitchen, extract_furnished, extract_fireplaces, extract_terrace, extract_terrace_area, extract_garden, extract_garden_area, extract_swimming_pool, extract_land_surface, extract_number_of_facades, extract_construction_year, extract_peb, extract_energy_consumption, extract_building_state
import time
import re

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

# Asynchronous function to scrape a single Immoweb page
async def scrape_immoweb_page(session, url):
    headers = {'User-Agent': get_random_user_agent()}
    
    try:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            if soup:
        # Find all <a> tags with href attributes
                links = soup.find_all('a', href=True)
        
        # Filter links based on specific criteria
                filtered_links = [
                    link['href'] for link in links 
                    if len(link['href'].split("/")) > 8  
                    ]
        
        return filtered_links
            

       
    except Exception as e:
        print(f"Error scraping {url}: {e}", end='\r')
        return None

# Main asynchronous function to scrape multiple pages concurrently
async def main(url_list, output_file):
    immoweb_data = []
    timeout = aiohttp.ClientTimeout(total=3600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [scrape_immoweb_page(session, url) for url in url_list]
        
        for index, task in enumerate(asyncio.as_completed(tasks)):
            data = await task
            if data:
                for link in data:
                    immoweb_data.append({'Links': link})
                    print(f'Data extraction: {index+1}/{len(tasks)} pages loaded',end='\r')

    # Save to DataFrame and CSV
    df = pd.DataFrame(immoweb_data)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Run the asynchronous scraping and save to CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
scraping_links_path = os.path.join(script_dir, '../csv_files/scraping_links.csv')

output_csv_file = scraping_links_path

url_list = []
for page_num in range(334):
        url_list.append(f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minPrice=50000&maxPrice=3000000&minSurface=30&maxSurface=150&isAPublicSale=false&isALifeAnnuitySale=false&isNewlyBuilt=false&page={page_num}&orderBy=relevance')
for page_num in range(334):
        url_list.append(f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minPrice=50000&maxPrice=3000000&minSurface=150&maxSurface=400&isAPublicSale=false&isALifeAnnuitySale=false&isNewlyBuilt=false&page={page_num}&orderBy=relevance')        
for page_num in range(334):
        url_list.append(f'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&minPrice=50000&maxPrice=3000000&minSurface=400&maxSurface=1000&isAPublicSale=false&isALifeAnnuitySale=false&isNewlyBuilt=false&page={page_num}&orderBy=relevance')        

# Run the asyncio event loop
start_time = time.time()
asyncio.run(main(url_list, output_csv_file))
end_time = time.time()
print(end_time - start_time)