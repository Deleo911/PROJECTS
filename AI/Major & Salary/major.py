from email.headerregistry import Group
from tokenize import group
import pandas as pd
import os

# To collect the csv file and to have access
csv_path = os.path.join(os.path.dirname(__file__), "salaries_by_college_major.csv")
df = pd.read_csv(csv_path)
# To get first 5 rows from the csv file
df.head()
# To get the size or dimention of the csv file
df.shape
# To get all the attributes names of the csv file
df.columns
# To check if the is any non filled cell or data type error
df.isna()
# To get lass 5 rows from the csv file
df.tail()
# To delete any row that has NaN(Not a Number)
clean_df = df.dropna()
# clean_df now contain data that is void of error
clean_df.tail()
# To access particular column in the csv file we can use square bracket notation
clean_df['Starting Median Salary']
# To get the highest Starting Median Salary
clean_df['Starting Median Salary'].max()
# To get the row number or index of this highest Starting Median Salary
n=clean_df['Starting Median Salary'].idxmax()
# To get the major name that has this highest Starting Median Salary
clean_df['Undergraduate Major'].loc[n]
clean_df['Undergraduate Major'][n]
# To get all the row of that index
clean_df.loc[n]
# To add another attribute with name Spread
info=clean_df['Mid-Career 90th Percentile Salary'].subtract(clean_df['Mid-Career 10th Percentile Salary'])
clean_df.insert(1,"Spread",info)
# Sort in ascending risk
lr=clean_df.sort_values("Spread")
lr[['Undergraduate Major','Spread']]
# Grouping in categories
clean_df.groupby("Group")
# To count the elements of each group
clean_df.groupby("Group").count()
# To find the mean of each group
clean_df.groupby("Group").mean(numeric_only=True)
# To change format of number
# pd.options.display.float_format = '{:,.2f}'.format
print(clean_df.groupby("Group").mean(numeric_only=True))