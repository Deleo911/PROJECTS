import pandas as pd

df=pd.read_csv("/100DAYS/Day71/salaries_by_college_major.csv")
cleandf=df.dropna()

# What college major has the highest mid career salary?
n1=cleandf['Mid-Career Median Salary'].idxmax()
ans1=cleandf['Undergraduate Major'].loc[n1]
print(f"The college with the highest mid career salary is {ans1}")
# How much do graduates with this major earn?
ans2=cleandf['Starting Median Salary'][n1]
print(f"The graduate earn {ans2}")

# Which college major has the lowest starting salary and how much do graduates earn after university?
n2=cleandf['Starting Median Salary'].idxmin()
ans3=cleandf['Undergraduate Minor'].loc[n2]
print(f"The college with the lowest starting salary is {ans3}")
ans4=cleandf['Mid-Career 10th Percentile Salary'][n2]+cleandf['Mid-Career 90th Percentile Salary'][n2] 
print(f"Graduate at the end of university end {ans4}")

# Which college major has the lowest mid-career salary and how much can people expect to earn with this degree? 
n3=cleandf['Mid-Career Median Salary'].idxmin()
ans5=cleandf['Undergraduate Major'].loc[n3]
print(f"The college with the lowest mid career salary is {ans5}")
ans6=cleandf['Starting Median Salary'][n3]
print(f"The graduate earn {ans6}")