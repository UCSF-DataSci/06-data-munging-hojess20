# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: [125718]
- **Columns**: [5]

### Column Details
| Column Name     | Data Type | Non-Null Count | Unique Values | Mean      |
|------------------|-----------|----------------|---------------|-----------|
| income_groups     | object    | 119412         | 8             | n/a     |
| age               | float     | 119495         | 101           | 50.01     |
| gender            | float     | 119811         | 3             | 1.58      |
| year              | float     | 119516         | 169           | 2025.07   |
| population        | float     | 119378         | 114925        | 1.11e+08  |

### Identified Issues
1. **Duplicate data**
There are duplicate rows of data. All columns have duplicate values, and this would impact summary statistics and 
overall analyses done on this data.
duplicates = df.duplicated().sum()


2. **Missing data**
There are missing values in all of the columns (below is the number of missing values for each column):
income_groups    6306
age              6223
gender           5907
year             6202
population       6340
The missing data can cause errors in future analyses.

3. **Wrong data types**
The data types for year and population should be changed from a string to numerical. Loading the data into pandas 
converted these columns to the appropriate data types (numeric.) 
The data types of each column after loading in the data is:
income_groups     object
age              float64
gender           float64
year             float64
population       float64
dtype: object
Inappropriate data types would lead to erroneous summary statistics and make it difficult to conduct meaningful 
analyses.

4. **Invalid data values**
There are entries within the income groups that are unlabeled (blank) or labeled as "high_income_typo" ,  
"low_income_typo”. Additionally, the gender column has an additional category of 3, which should be addressed. Also, 
there are years beyond 2024 that should be invalid since it is impossible to collect future data.

Unique values in 'Income_Group' column:
['high_income' 'high_income_typo' 'low_income' 'low_income_typo'
 'lower_middle_income' 'lower_middle_income_typo'
 'upper_middle_income_typo' 'upper_middle_income']

Unique values in gender:
 gender
1.0    56777
2.0    56748
3.0     6286
Incorrect data values can severely impact our analyses, leading to false narratives and inaccurate results.

5. **Outliers **
The population has a very large range of values, where there are seemingly outliers on both ends of the spectrum. Most 
values are 7 digits long, but some population values are only 2 digits or over 9 digits long. The extreme values would 
skew the actual distribution of population data, impacting potential analyses and leading to inaccurate conclusions. 


## 2. Data Cleaning Process

1. **Duplicate data**
I identified and removed all the duplicate data since we already 1 set of each row.
- **Implementation**: df = df.drop_duplicates()
There were 2950 rows of duplicate data that were dropped. Removing these provide a clearer distribution of each column 
data, and prevent any skewing of summary statistics (e.g. mean, median, frequency).

2. **Missing data**
I dropped all row with missing data. This includes rows that were left blank since it would be impossible to fill in the 
blanks with the actual income group without additional information. This is the best method since the data set is large 
enough that losing the rows with missing data would not lead to too big of a loss in statistical power. Also it provides 
a more accurate and complete depiction of the data.
- **Implementation**: df = df.dropna()
This trimmed the data frame down 27343 rows (after the duplicate removal), leaving 95425 rows remaining.

3. **Data types**
It would be more meaningful to convert gender from numeric to a categorical variable since there are pre-defined 
categories. It is possible statistical tools or algorithms may treat it as a continuous variable which would lead to 
incorrect statistical analyses (calculating the mean).
- **Implementation**: df_cleaner['gender'] = df_cleaner['gender'].astype('category')
All 95425 rows in the data frame would be affected since the data type of each gender entry is changed. The data 
distribution did not change.

4. **Invalid data values**
I restructured the categories for income_groups. For example, ‘high_income_typo’ would be treated as ‘high_income’ and 
‘low_income_typo’ would be grouped with ‘low_income’ as one category. This will make interpreting income data easier. 
The data distribution would remain the same since only the typo values were just mapped to the correct category. 
- **Implementation**:
income_group_mapping = {
    'high_income_typo': 'high_income',
    'low_income_typo': 'low_income',
    'upper_middle_income_typo': 'upper_middle_income',
    'lower_middle_income_typo': 'lower_middle_income'
    }
    df_cleaner['income_groups'] = df_cleaner['income_groups'].replace(income_group_mapping)

To handle data where gender = 3, I opted to remove these rows. 
- **Implementation**: 
df_cleaner = df_cleaner[df_cleaner['gender'] != 3]

A value of 3 could either be a mistake or it could represent a non-binary gender, but without additional information, 
the best option is to remove these rows. This provides a more complete dataset with data we know to be accurate. Also, 
there are 6286 of rows where gender is equal to 3, so dropping these rows would still leave sufficiently sized data 
frame. The gender distribution remains the same among 1s and 2s.

5. **Outliers**
To deal with the outliers in the population data, I calculated the IQR boundaries to determine which values would be 
treated as outliers. This was the most suitable strategy to measure data spread that is less influenced by extreme 
values. 
- **Implementation**:
Q1 = df['population'].quantile(0.25)
Q3 = df['population'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_cleaner = df_cleaner[(df_cleaner['population'] < lower_bound) | (df_cleaner['population'] > upper_bound)]
By doing this, the mean, standard deviation, and median of the population distribution have shifted. The uncleaned 
population data had a mean of 8.781311e+07. It is now 6.344829e+06. Overall, the data spread is more accurate, as there 
are now less extreme values on both ends of the distribution. This removed 876 outlier rows.


## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv
- **Rows**: [43895]
- **Columns**: [5]

| Column Name     | Data Type | Non-Null Count | Unique Values | Mean          |
|------------------|-----------|----------------|---------------|---------------|
| income_groups     | object    | 43895          | 4             | n/a           |
| age               | float64   | 43895          | 101           | 50.19         |
| gender            | category  | 43895          | 2             | n/a           |
| year              | float64   | 43895          | 75            | 1987          |
| population        | float64   | 43895          | 43325         | 6344829.13    |

- This cleaned data no longer has duplicate rows, missing values (NaN), outliers, and unwanted or erroneous data values. 
It no longer has inappropriate data types and mislabeled values are recategorized. By handling these messy issues, it 
reduced the original dataset by over 50%. The original dataset had 125718 rows, whereas this cleaned dataset has only 
43895 rows. Despite this mass reduction, the data is more complete and accurate, which will result in more truthful 
analyses. 
- The main challenge in this assignment was determining the ‘messy’ aspects of the data. There is a lot of ambiguity, 
especially without a codebook or data dictionary or even context on what the dataset is on made it difficult to discern 
if certain values were mistakes or intentional. 
- In terms of next steps or improvements: testing other methods for handling outliers might provide a more balanced 
view, particularly if some extreme values carry real-world significance. Implementing additional data checks (thresholds 
for reasonable age or population values) before analysis could prevent unrealistic values possibly slipping through.

