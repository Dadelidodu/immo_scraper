import re

def extract_locality(url):
    match = re.search(r'for-sale/([^/]+)/', url)
    if match:
        locality_name = match.group(1)
        cleaned_locality = re.sub(r'[^a-zA-Z\s-]', '', locality_name)
        if cleaned_locality.endswith('-'):
            cleaned_locality = cleaned_locality[:-1]
        return cleaned_locality.capitalize()
    return None

def extract_zipcode(url):
    url_list = url.split("/")
    zipcode = url_list[8]
    if zipcode:
        return int(zipcode)
    else:
        return None

def extract_living_area(soup):
    overview_columns = soup.find_all('div', class_='overview__column')
    if len(overview_columns) > 1:
        overview_items = overview_columns[1].find_all('div', class_='overview__item')
        if overview_items:
            item_text = overview_items[0].get_text(strip=True)
            cleaned_text = re.sub(r'\D', '', item_text)
            return cleaned_text if cleaned_text else None
    return None

def extract_land_surface(soup):
    overview_columns = soup.find_all('div', class_='overview__column')
    if len(overview_columns) > 1:
        overview_items = overview_columns[1].find_all('div', class_='overview__item')
        if len(overview_items) > 1:
            item_text = overview_items[1].get_text(strip=True)
            cleaned_text = re.sub(r'\D', '', item_text)
            return cleaned_text
        else:
            return None
    return None

def extract_price(soup):
    elem_div = soup.find("div", class_="classified__header-primary-info")
    if elem_div:
        elem_price = elem_div.find("p", class_ = "classified__price")
        if elem_price:
            true_price = elem_price.find('span', {'aria-hidden': 'true'})
            if true_price:
                true_price = true_price.get_text(strip=True)
                cleaned_text = re.sub(r'\D', '', true_price)
                return cleaned_text
            else:
                return None
        else:
            return None
    else:
        return None
    
def extract_numbers_of_rooms(soup):
    overview_columns = soup.find_all('div', class_='overview__column')
    if len(overview_columns) > 1:
        overview_items = overview_columns[0].find_all('div', class_='overview__item')
        if overview_items:
            item_text = overview_items[0].get_text(strip=True)
            cleaned_text = re.sub(r'\D', '', item_text)
            return cleaned_text if cleaned_text else None
    return None

def extract_property_subtype(url):
    match = re.search(r'classified/([^/]+)/', url)
    property_type = match.group(1)
    if match:
        return property_type
    else:
        return None

def extract_property_type(url):
    property_type = extract_property_subtype(url)
    houses = ["house", "bungalow", "castle", "country-house", "mixed-use-building", 
              "country-cottage", "apartment-block", "town-house", "villa", "manor-house", 
              "chalet", "farmhouse", "exceptional-property", "mansion", "other-properties", "pavilion", "other-property"]
    apartments = ["apartment", "ground-floor", "triplex", "penthouse", 
                  "kot", "duplex", "studio", "loft", "service-flat", "flat-studio"]
    
    if property_type in houses:
        return 'House'
    elif property_type in apartments:
        return 'Apartment'
    else:
        return None

def extract_sale_type(url):
    url_list = url.split("/")
    sale_type = url_list[6]
    if sale_type:
        return sale_type
    else:
        return None
    

def extract_equiped_kitchen(block_content):
    if block_content:
        
        # Check for 'Hyper equipped' or 'Installed' in the block content
        if re.search(r'Hyper equipped|Installed', block_content, re.IGNORECASE):
            return 1
        else:
            return 0
    return 0

def extract_furnished(block_content):
    if block_content:
        
        # Check if "Furnished" is in the content
        if re.search(r'Furnished', block_content, re.IGNORECASE):
            # Pattern to capture content between <td class="classified-table__data"> and </td>
            pattern = r'Furnished</th>\s*<td class="classified-table__data">\s*(.*?)\s*</td>'
            match = re.search(pattern, block_content, re.IGNORECASE)
            
            # Return 1 if the content is "Yes", else return 0
            if match and match != None and match.group(1).strip().lower() == "yes":
                return 1
            else:
                return 0
    return 0

def extract_fireplaces(block_content):
    if block_content:
        
        if re.search(r'How many fireplaces\?', block_content, re.IGNORECASE):

            pattern = r'How many fireplaces\?</th>\s*<td class="classified-table__data">\s*(\d+)\s*</td>'
            match = re.search(pattern, block_content)
            if match and match != None:
                return 1 if match else 0
    return 0

def extract_terrace_area(block_content):
    if block_content:
        
        if re.search(r'Terrace surface', block_content, re.IGNORECASE):
            
            pattern = r'Terrace surface</th>\s*<td class="classified-table__data">\s*(\d+)\s*'
            match = re.search(pattern, block_content, re.DOTALL)
            if match and match != None:
                return int(match.group(1)) if match else None
    return None

def extract_terrace(soup):
    
    terrace_area = extract_terrace_area(soup)
        
    if terrace_area != 0 and terrace_area != None:
        return 1
    else:
        return 0
        
def extract_garden_area(block_content):
    if block_content:
        
        if re.search(r'Garden surface', block_content, re.IGNORECASE):

            pattern = r'Garden surface</th>\s*<td class="classified-table__data">\s*(\d+)\s*'
            match = re.search(pattern, block_content, re.DOTALL)
            if match and match != None:
                return int(match.group(1)) if match else None
    return None

def extract_garden(soup):
    
    garden_area = extract_garden_area(soup)
    
    if garden_area != 0 and garden_area != None:
        return 1
    else:
        return 0   
    
def extract_number_of_facades(block_content):
    if block_content:
        
        # Search for the label "Number of frontages" with possible spaces around it
        if re.search(r'Number of frontages', block_content, re.IGNORECASE):
            
            # Adjusted regex pattern to match the number in <td> associated with "Number of frontages"
            pattern = r'<th[^>]*>\s*Number of frontages\s*</th>\s*<td class="classified-table__data">\s*(\d+)\s*</td>'
            match = re.search(pattern, block_content, re.DOTALL)
            if match and match != None:
            
                return int(match.group(1)) if match else None
    return None

def extract_construction_year(block_content):
    if block_content:
        
        # Search for the label "Number of frontages" with possible spaces around it
        if re.search(r'Construction year', block_content, re.IGNORECASE):
            
            # Adjusted regex pattern to match the number in <td> associated with "Number of frontages"
            pattern = r'<th[^>]*>\s*Construction year\s*</th>\s*<td class="classified-table__data">\s*(\d+)\s*</td>'
            match = re.search(pattern, block_content, re.DOTALL)
            if match and match != None:
                birth_year = int(match.group(1)) 
                return birth_year if birth_year else None
    return None

def extract_peb(block_content):
    if block_content:
        
        
        if re.search(r'Energy class', block_content, re.IGNORECASE):
            
            pattern = r'Energy class</th>\s*<td class="classified-table__data">\s*(\S+)\s*</td>'
            match = re.search(pattern, block_content, re.DOTALL)
            
            if match and match.group(1).strip().upper() in ['A','B', 'C', 'D', 'E', 'F', 'G']:
                return match.group(1)
            else:
                return None
    return None

def extract_energy_consumption(block_content):
    if block_content:
        
        # Check if "Primary energy consumption" is in the content
        if re.search(r'Primary energy consumption', block_content, re.IGNORECASE):
            
            # Adjusted pattern to match only the numeric part in <td> associated with "Primary energy consumption"
            pattern = r'Primary energy consumption</th>\s*<td class="classified-table__data">\s*(\d+)\s*'
            match = re.search(pattern, block_content, re.DOTALL)
            
            if match:
                return int(match.group(1).strip())
            else:
                return None
    return None


def extract_building_state(block_content):
    if block_content:
        
        # Search for the label "Number of frontages" with possible spaces around it
        if re.search(r'Building condition', block_content, re.IGNORECASE):
            
            # Adjusted regex pattern to match the number in <td> associated with "Number of frontages"
            pattern = r'<th[^>]*>\s*Building condition\s*</th>\s*<td class="classified-table__data">\s*(.*?)\s*</td>'
            match = re.search(pattern, block_content, re.DOTALL)
            if match:
                return match.group(1).strip() if match else None
    return None

def extract_swimming_pool(block_content):
    if block_content:
        
        # Search for the label "Number of frontages" with possible spaces around it
        if re.search(r'Swimming pool', block_content, re.IGNORECASE):
            
            # Adjusted regex pattern to match the number in <td> associated with "Number of frontages"
            pattern = r'<th[^>]*>\s*Swimming pool\s*</th>\s*<td class="classified-table__data">\s*(.*?)\s*</td>'
            match = re.search(pattern, block_content, re.DOTALL)
            
            if match != None and match.group(1).strip() == 'Yes':
                return 1
            else:
                return 0
    return 0
