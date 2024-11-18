import random
import os
import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from extract_functions import extract_locality, extract_zipcode, extract_property_type, extract_property_subtype, extract_price, extract_sale_type, extract_numbers_of_rooms, extract_living_area, extract_equiped_kitchen, extract_furnished, extract_fireplaces, extract_terrace, extract_terrace_area, extract_garden, extract_garden_area, extract_swimming_pool, extract_land_surface, extract_number_of_facades, extract_construction_year, extract_peb, extract_energy_consumption, extract_building_state
import time

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
    error_count = 0
    try:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            body = soup.find('div', class_="container container--body")
            if body:
                blocks = body.find_all('div', class_="text-block")
                block_content = str(blocks)
            

        data = {
            'Locality': extract_locality(url),
            'Zip Code': extract_zipcode(url),
            'Type of Property': extract_property_type(url),
            'Subtype of Property': extract_property_subtype(url),
            'Price': extract_price(soup),
            'Type of Sale': extract_sale_type(url),
            'Number of Rooms': extract_numbers_of_rooms(soup),
            'Livable Space (m2)': extract_living_area(soup),
            'Fully Equipped Kitchen': extract_equiped_kitchen(block_content),
            'Furnished': extract_furnished(block_content),
            'Any Fireplace ?': extract_fireplaces(block_content),
            'Terrace': extract_terrace(block_content),                       
            'Terrace Area (m2)': extract_terrace_area(block_content),         
            'Garden': extract_garden(block_content),                          
            'Garden Area (m2)': extract_garden_area(block_content),
            'Swimming Pool': extract_swimming_pool(block_content),           
            'Surface of the Land (m2)': extract_land_surface(soup),
            'Number of Facades': extract_number_of_facades(block_content),
            'Construction Year': extract_construction_year(block_content),
            'PEB': extract_peb(block_content),
            'Primary Energy Consumption (kWh/m2)': extract_energy_consumption(block_content),        
            'State of the Building': extract_building_state(block_content),
            'Url': url  
        }
        
        return data
    except Exception as e:
        error_count += 1
        print(f"Error scraping {url}: {e}, {error_count}", end='\r')
        return None

# Main asynchronous function to scrape multiple pages concurrently
async def main(url_list, output_file):
    immoweb_data = []
    timeout = aiohttp.ClientTimeout(total=5000)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [scrape_immoweb_page(session, url) for url in url_list]
        
        for index, task in enumerate(asyncio.as_completed(tasks)):
            data = await task
            if data:
                immoweb_data.append(data)
                print(f'Data extraction: {index+1}/{len(tasks)} pages loaded',end='\r')

    # Save to DataFrame and CSV
    df = pd.DataFrame(immoweb_data)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Run the asynchronous scraping and save to CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
scraping_results_path = os.path.join(script_dir, '../csv_files/scraping_results.csv')
cleaned_links_path = os.path.join(script_dir, '../csv_files/cleaned_links.csv')

output_csv_file = scraping_results_path
link_df = pd.read_csv(cleaned_links_path)
url_list = link_df['Links'].tolist()

# Run the asyncio event loop
start_time = time.time()
asyncio.run(main(url_list, output_csv_file))
end_time = time.time()
print(end_time - start_time)