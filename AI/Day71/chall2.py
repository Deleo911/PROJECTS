import pandas as pd

df=pd.read_csv('salaries_by_college_major.csv')
cleandf=df.dropna()

# Using the .sort_values() method, can you find the degrees with the highest potential?
ans1=cleandf.sort_values(by=['Mid-Career 90th Percentile Salary'], ascending=False)['Undergraduate Major'][0]
print(f"The degree with the highest potential is {ans1}")
# Find the top 5 degrees with the highest values in the 90th percentile.
ans2=cleandf.sort_values(by=['Mid-Career 90th Percentile Salary'], ascending=False)['Undergraduate Major'].head()
print(f"The top 5 degrees with the highest values in the 90th is {ans2}")

# Find the degrees with the greatest spread in salaries.
n=cleandf['Spread'].idxmax()
ans3=cleandf['Undergraduate Major'][n]
print(f"The degrees with the greatest spread is {ans3}")
# Which majors have the largest difference between high and low earners after graduation.
ans4=cleandf.sort_values(by=['Mid-Career Median Salary'], ascending=False).head()
print(ans4)
