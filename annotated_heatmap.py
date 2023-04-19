import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('activities.csv')

# Add new columns for month and year parsed from the Activity Date column
df['month'] = pd.to_datetime(df['Activity Date']).dt.strftime('%b')
df['year'] = pd.to_datetime(df['Activity Date']).dt.year

# Filter to only include data from 2017-2023
df = df[(df['year'] >= 2017) & (df['year'] <= 2023)]

# Create a custom order for the months
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Convert the "month" column to a Categorical data type with the custom order
df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

# Set the index column (if applicable)
# df.set_index('column_name', inplace=True)

# Create a pivot table with desired rows and columns
# Replace 'value_column_name' with the column you want to plot
pivot = pd.pivot_table(df, index='month', columns='year', values='Relative Effort', aggfunc='sum')

# Plot the pivot table as a heatmap
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(pivot, annot = True, fmt = ',.0f', linewidths=.7, ax=ax, cmap='Reds', cbar_kws={'label': 'Total Monthly Relative Effort'})

# Save plot as PNG
plt.savefig('relative_effort_heatmap.png', dpi=300)

# Show the plot
plt.show()