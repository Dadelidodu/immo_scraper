import pandas as pd
import os

# Read the CSV file into a DataFrame
script_dir = os.path.dirname(os.path.abspath(__file__))
extracted_links_path = os.path.join(script_dir, '../csv_files/scraping_links.csv')
df = pd.read_csv(extracted_links_path)

# Filter the DataFrame to keep only the rows where 'Links' starts with "https://www.immoweb.be/"
df = df[df['Links'].str.startswith('https://www.immoweb.be/')]

# Remove duplicate links
df = df.drop_duplicates(subset='Links')

# Display the first few rows of the updated DataFrame
print(df.head())

# If needed, you can save the cleaned DataFrame to a new CSV file
cleaned_links_path = os.path.join(script_dir, '../csv_files/cleaned_links.csv')
df.to_csv(cleaned_links_path, index=False)