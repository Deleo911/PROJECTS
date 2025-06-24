import pandas as pd
import os

# Load the dataset
csv_path = os.path.join(os.path.dirname(__file__), "salaries_by_college_major.csv")
df = pd.read_csv(csv_path)

# Drop missing values
cleandf = df.dropna()

# (Optional) Create a 'Spread' column if not already in the dataset
if 'Spread' not in cleandf.columns:
    cleandf['Spread'] = cleandf['Mid-Career 90th Percentile Salary'] - cleandf['Starting Median Salary']

# 1. Find the degree with the highest 90th percentile salary
ans1 = cleandf.sort_values(by='Mid-Career 90th Percentile Salary', ascending=False)['Undergraduate Major'].iloc[0]
print(f"The degree with the highest potential is: {ans1}")

# 2. Top 5 degrees by 90th percentile salary
ans2 = cleandf.sort_values(by='Mid-Career 90th Percentile Salary', ascending=False)['Undergraduate Major'].head()
print("Top 5 degrees with the highest 90th percentile salaries:")
print(ans2.to_string(index=False))

# 3. Degree with the greatest salary spread
max_spread_idx = cleandf['Spread'].idxmax()
ans3 = cleandf.loc[max_spread_idx, 'Undergraduate Major']
print(f"The degree with the greatest salary spread is: {ans3}")

# 4. Top 5 majors by Mid-Career Median Salary
ans4 = cleandf.sort_values(by='Mid-Career Median Salary', ascending=False).head()
print("Top 5 majors with the highest Mid-Career Median Salary:")
print(ans4[['Undergraduate Major', 'Mid-Career Median Salary']].to_string(index=False))
