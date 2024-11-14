import pandas as pd
import os 



# Read the CSV file into a DataFrame
script_dir = os.path.dirname(os.path.abspath(__file__))
scraping_results_path = os.path.join(script_dir, '../csv_files/scraping_results.csv')
df = pd.read_csv(scraping_results_path)
# Apartment stats

df_apartment = df[df['Type of Property'] == 'Apartment']
print(df_apartment)
df_apartment_sorted = df_apartment.sort_values(by=['Zip Code', 'Price'], ascending=[True, True])
print(df_apartment_sorted)
price_stats_apartment = df_apartment_sorted.groupby('Zip Code', as_index=False)['Price'].agg(
    mean_price=('mean'),
    median_price=('median'),
    std_price=('std')
)
print(price_stats_apartment)


# Houses stats

df_house = df[df['Type of Property'] == 'House']
df_house_sorted = df_house.sort_values(by=['Zip Code', 'Price'], ascending=[True, True])
price_stats_house = df_house_sorted.groupby('Zip Code', as_index=False)['Price'].agg(
    mean_price=('mean'),
    median_price=('median'),
    std_price=('std')
)

# Heatmap building 

# apartment_heatmap_path = os.path.join(script_dir, '../csv_files/heatmap_data/apartments_heatmap_dataset.csv')
# house_heatmap_path = os.path.join(script_dir, '../csv_files/heatmap_data/houses_heatmap_dataset.csv')
# price_stats_apartment.to_csv(apartment_heatmap_path, index=False)
# price_stats_house.to_csv(house_heatmap_path, index=False)

# clean_dataset_path = os.path.join(script_dir, '../csv_files/cleaned_dataset.csv')
# df.to_csv(clean_dataset_path, index=False)