import pandas as pd
import os 

# Read the CSV file into a DataFrame
script_dir = os.path.dirname(os.path.abspath(__file__))
scraping_results_path = os.path.join(script_dir, '../csv_files/scraping_results.csv')
df = pd.read_csv(scraping_results_path)

#Cleaning

# Drop rows where either 'Price' or 'Number of Rooms' has missing values
df = df.dropna(subset=['Price', 'Number of Rooms'])

# Encode type of property (House = 1, Apartment = 0)
#df['Type of Property'] = df['Type of Property'].replace({'House': 1, 'Apartment': 0}).infer_objects(copy=False)

# Encode type of sales as numeric
df['Type of Sale'] = df['Type of Sale'].replace({'for-sale': 1}).infer_objects(copy=False)

# Find the index of the current 'Any Fireplace ?' column
fireplaces_index = df.columns.get_loc('Any Fireplace ?')

# Create the new 'Open Fire' column based on 'Any Fireplace ?'
df['Open Fire'] = df['Any Fireplace ?'].apply(lambda x: 0 if x == 0 else 1)

# Insert the new 'Open Fire' column at the same index
df.insert(fireplaces_index, 'Open Fire', df.pop('Open Fire'))
df = df.drop(columns=['Any Fireplace ?'])

# Replace missing values in the 'Number of Facades' columns with 0
df['Number of Facades'] = df['Number of Facades'].fillna(0)

# Replace 'Number of facades' with 1 where 'Type of Property' is 0 (apartment) and 'Number of facades' is 0
df.loc[(df['Type of Property'] == 0) & (df['Number of Facades'] == 0), 'Number of Facades'] = 1

# Replace 'Number of Facades' with 2 where 'Subtype of Property' is 'duplex' or 'town-house' and 'Number of Facades' is 0
df.loc[(df['Subtype of Property'].isin(['duplex', 'town-house'])) & (df['Number of Facades'] == 0), 'Number of Facades'] = 2

# Replace remaining 'Number of Facades' 0 values for remaining houses with 4
# Replace 'Number of Facades' with 4 where 'Type of Property' is 1 (House) and 'Number of Facades' is 0
df.loc[(df['Type of Property'] == 1) & (df['Number of Facades'] == 0), 'Number of Facades'] = 4

# Replace missing values in the 'Terrace Area (m2)' columns with 0
df['Terrace Area (m2)'] = df['Terrace Area (m2)'].fillna(0)

# Replace missing values in the 'Garden Area (m2)' columns with 0
df['Garden Area (m2)'] = df['Garden Area (m2)'].fillna(0)

# Replace missing values in the 'Surface of the Land (m2)' columns with 0
df['Surface of the Land (m2)'] = df['Surface of the Land (m2)'].fillna(0)

# Replace missing values in the 'Primary Energy Consumption (kWh/m2)' columns with mean value
df['Primary Energy Consumption (kWh/m2)'] = df['Primary Energy Consumption (kWh/m2)'].fillna(round(df['Primary Energy Consumption (kWh/m2)'].mean(), 1))

# Encode state of the building: Ordinal encoding, since categories have inherent order
state_mapping = {
    'To restore': 0,
    'To renovate': 1,
    'To be done up': 2,
    'Good': 3,
    'Just renovated': 4,
    'As new': 5
}

df['State of the Building'] = df['State of the Building'].replace(state_mapping)
df['State of the Building'] = df['State of the Building'].fillna(round(df['State of the Building'].mean(), 1))

# Encode PEB: Ordinal encoding, since categories have inherent order
PEB_mapping = {
    'G': 0,
    'F': 1,
    'E': 2,
    'D': 3,
    'C': 4,
    'B': 5,
    'A': 6
}

df['PEB'] = df['PEB'].replace(PEB_mapping)
df['PEB'] = df['PEB'].fillna(round(df['PEB'].mean(), 1))

# Drop the 'Url' column from the DataFrame (since not required and non-numerical values)
df = df.drop_duplicates(subset=df.columns.difference(['Url']))
df = df.drop(columns=['Url'])
df = df.drop(columns=['Construction Year'])


# Saving
clean_dataset_path = os.path.join(script_dir, '../cleaned_dataset.csv')
df.to_csv(clean_dataset_path, index=False)

clean_dataset_path = os.path.join(script_dir, '../csv_files/cleaned_dataset.csv')
df.to_csv(clean_dataset_path, index=False)