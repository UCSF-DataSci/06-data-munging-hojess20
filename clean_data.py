import pandas as pd
import numpy as np
import logging

# Set up logging to track the cleaning process
logging.basicConfig(filename='cleaning_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(input_file, output_file):
    df = pd.read_csv(input_file)
    logging.info("Loaded in messy data")

    # Removing duplicates
    df_size = df.shape
    df_clean = df.drop_duplicates()
    logging.info(f"Removed duplicates: {df_size[0] - df_clean.shape[0]} rows removed.")
    
    # Removing missing values from data frame without dupicates
    missing_summary = df.isnull().sum()
    logging.info(f"Removed missing values in data frame. Missing values per column:\n{missing_summary}")
    df_clean['income_groups'].replace("", np.nan, inplace=True)
    df_cleaner = df_clean.dropna()

    # Changing data type
    data_type = df_clean.dtypes
    df_cleaner['gender'] = df_cleaner['gender'].astype('category')
    logging.info(f"Data types:\n{data_type} \nUpdated gender data type:\n{df_cleaner.dtypes}")

    # Refactoring typo income group values to correct income group
    unique_values = df_cleaner['income_groups'].unique()
    print(unique_values)

    income_group_mapping = {
    'high_income_typo': 'high_income',
    'low_income_typo': 'low_income',
    'upper_middle_income_typo': 'upper_middle_income',
    'lower_middle_income_typo': 'lower_middle_income'
    }

    # Replace the typos with correct values
    df_cleaner['income_groups'] = df_cleaner['income_groups'].replace(income_group_mapping)
    logging.info(f"Remapped income group typos to their corresponding non-typo income group. Unique values in income_groups: {df_cleaner['income_groups'].unique()}")

    # Remove gender ==3 and years > 2024
    df_cleaner = df_cleaner[df_cleaner['gender'] != 3]
    df_cleaner = df_cleaner[df_cleaner['year'] <= 2024]
    logging.info(f"Removed gender == 3 values and filtered out years beyond 2024")

    # Finding outlier boundaries
    Q1 = df['population'].quantile(0.25)
    Q3 = df['population'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    messypop_row_count = df_cleaner.shape[0] 

    # Filter out outliers
    df_cleaner = df_cleaner[(df_cleaner['population'] >= lower_bound) & (df_cleaner['population'] <= upper_bound)]

    # Calculate messy populatoin rows removed
    rows_removed = messypop_row_count - df_cleaner.shape[0]
    logging.info(f"Filtered out population values outside of the lower and upper boundaries for outliers. Removed {rows_removed} rows.")

    # print(df_cleaner.info())
  
    df_cleaner.to_csv(output_file, index=False)
    logging.info(f"Cleaned data saved to {output_file}")
    
if __name__ == "__main__":
    # Specify input and output files
    input_file = "messy_population_data.csv"
    output_file = "cleaned_population_data.csv"
    
    # Run the cleaning process
    clean_data(input_file, output_file)

    