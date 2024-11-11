import pandas as pd
import numpy as np
import re


##engine column from used_cars.csv was too complex (some had HP, number of cylinders, and the liters)
##as a result, the following functions extracts any information relevant to cylinders and liters
##to split the engine column into only cylinders and liters (dropping horseopower as a column)

#extracting liters from the engine column as a float type
def extract_liters(engine_str):
    #matching keywords to find information regarding "liter" in the engine string value
    match = re.search(r"(\d+\.\d+)L|(\d+\.\d+) Liter", str(engine_str), re.IGNORECASE)
    if match:
        return float(match.group(1) or match.group(2))
    #999 was chosen as the unique identifier to define any blank or unknown values in the dataset
    return 999  

#extracting cylinders from the engine column as an int type
def extract_cylinders(engine_str):
    #matching keyword to find information regarding "cylinder" in the engine string value
    match = re.search(r"V-?(\d+)|l(\d+)|(\d+) Cylinder", str(engine_str), re.IGNORECASE)
    if match:
        return int(match.group(1) or match.group(2) or match.group(3))
    return 999  

#for the purpose of making the data easier to access and work with, I decided to simplify the
#tranmission column into only th etype of transmission (Ex: "Automatic", "Manual", etc) and getting
#rid of any speed related to the tranmssion so the model can interept the data easier
def simplify_transmission(transmission_str):
    
    transmission_str = str(transmission_str).lower()
    #matching common abbreviations found in the dataset
    if "automatic" in transmission_str or "a/t" in transmission_str:
        return "Automatic"
    elif "manual" in transmission_str or "m/t" in transmission_str:
        return "Manual"
    elif "cvt" in transmission_str:
        return "CVT"
    else:
        return "Other"

#received help via ai to help determine how to encode and map all values, that way the user
#has access to the mappings of all data
#the following code has been ai generated:
def label_encode_column(data, column, output_file):
    """Encodes a column using Label Encoding and saves the mapping."""
    data[column] = pd.Categorical(data[column])
    mapping_dict = {category: code for code, category in enumerate(data[column].cat.categories)}
    mapping_df = pd.DataFrame(list(mapping_dict.items()), columns=[f'original_{column}', f'{column}_encoded'])
    mapping_df.to_csv(output_file, index=False)
    print(f"Mapping for '{column}' saved to '{output_file}'")
    data[column] = data[column].cat.codes
    data[column].replace(-1, np.nan, inplace=True)
    return mapping_dict

#developed a function to clean data from use_cars.csv to cleaned_used_cars.csv 
#this was a crucuial step as I used the random forest regression model which relies on 
#numerical values
def clean_data(input_file, output_file):
    #loaded in the used_cars.csv file first to begin the cleaning
    data = pd.read_csv(input_file)
    print("used_cars.csv has loaded in.\n")

    #In the used_cars.csv I noticed that some values had a value of "‚Äì" and blanks as well.
    #This may be an issue from the soruce downloaded, but I decided to treat both the same as they 
    #are unknown values and made them had a value of 999 as the model had issues interpreting
    #data with a null value at first. 
    data.replace("‚Äì", 999, inplace=True)
    data.fillna(999, inplace=True)

    #since the random forest regression model relies on numerical data, I converted
    #mileage to numerical data since it was in a string at first
    data['mileage'] = data['mileage'].str.replace(' mi.', '').str.replace(',', '').astype(float)

    #similiar to mileage, all I had to do was get rid of "$" sign to turn it into a numerical value
    data['price'] = data['price'].str.replace('$', '').str.replace(',', '').astype(float)

    #This part of the code was developed by ai as it allowed for the mapping of the data for the 
    #purpose of label encoding. 
    columns_to_map = ['brand', 'model', 'fuel_type', 'accident']
    mappings = {}
    for column in columns_to_map:
        mappings[column] = label_encode_column(data, column, f"{column}_mapping.csv")

    #for the clean_title data any car with a clean title was labeled as "Yes" and those without a 
    #clear title were left blank. Hence, I decided to replace "Yes" values with 1 and empty ones as 0.
    data['clean_title'] = data['clean_title'].apply(lambda x: 1 if x == "Yes" else 0)

    #since I needed to split the engine column into two columns, one for liters and one for cylinders,
    #the following code creates two new columns for them
    data['liters'] = data['engine'].apply(extract_liters)
    data['cylinders'] = data['engine'].apply(extract_cylinders)

    #I wanted the liters column to be represented as a float since liters share a pattern
    #of being represeted as floats in the data, and so I made any replaced int values "999" to be
    #"999.0" to avoid any issues if possible
    data['liters'] = data['liters'].astype(float)
    data['liters'].replace(999, 999.0, inplace=True)

    #dropped the engine column since it is now split into two "liters" and "cylinders"
    data.drop('engine', axis=1, inplace=True)

    #this part was also ai generated as it regards to mapping and label encoding of the transmission
    #column:
    data['transmission'] = data['transmission'].apply(simplify_transmission)
    transmission_mapping = label_encode_column(data, 'transmission', 'maps/transmission_mapping.csv')

    #Initially, I ran into several issues when developing the gui as it appeared the price_predictor.py 
    #first had to save the mapped values since on the gui I showed the string values, but the model only
    #uses numerical data, so I had to save the mapped numerical value of these strings to use in the
    #price_predictor.py file. As a result, ai suggested using reverse mapping which is shown below:
    fuel_mapping_reverse = {v: k for k, v in mappings['fuel_type'].items()}
    transmission_mapping_reverse = {v: k for k, v in transmission_mapping.items()}

    pd.DataFrame(list(fuel_mapping_reverse.items()), columns=['fuel_encoded', 'fuel_type']).to_csv('maps/fuel_mapping.csv', index=False)
    pd.DataFrame(list(transmission_mapping_reverse.items()), columns=['transmission_encoded', 'transmission']).to_csv('maps/transmission_mapping.csv', index=False)

    #I initially wanted to keep the int_col and ext_col columns in the cleaned data set but I realized
    #there was too much variety and many color names had names which were hard for identitfying them.
    #To understand better here's an example. Entry dataset 53 in the used_cars csv has the 
    #name "Mountain Air Metallic" as the ext_col, and this can cause confusion as it is hard to tell 
    #what exact color it is (gray, blue, etc).
    #This is just one example, but many data values in the used_cars.csv had this pattern of using
    #uncommon names and so I did not want to make any assumptions and instead decided to drop both columns
    #to avoid inaccurate data the cleaning of colors may do.
    if 'int_col' in data.columns:
        data.drop('int_col', axis=1, inplace=True)
    if 'ext_col' in data.columns:
        data.drop('ext_col', axis=1, inplace=True)

    #cleaned data needed to be saved to its own csv file so it only contained numerical data:
    data.to_csv(output_file, index=False)
    print(f"The cleaned (numerical) data has been saved :)'{output_file}'")

#finally, to run the cleaner.py file, I decided on making it simple for the user to see the differnce in 
#file names, so I used "cleaned_used_cars.csv" for the cleaned data. 
if __name__ == "__main__":
    clean_data('used_cars.csv', 'cleaned_used_cars.csv')
