import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load the data
activities = pd.read_csv('activities.csv')

# Convert the Activity Date to a pandas datetime object
activities['Activity Date'] = pd.to_datetime(activities['Activity Date'])

# Filter activities to only include those from 2018-2023
activities = activities[activities['Activity Date'].dt.year.isin(range(2018, 2024))]

# Compute the daily mean relative effort 
activities_daily = activities.groupby(pd.Grouper(key='Activity Date', freq='D')).sum()
activities_daily['14-day Moving Average'] = activities_daily['Relative Effort'].rolling(window=14).mean()
activities_daily['30-day Moving Average'] = activities_daily['Relative Effort'].rolling(window=30).mean()

# Create a figure with 6 subplots
fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(9, 12))

# Define the x-axis label format
date_fmt = mdates.DateFormatter('%b')

# Plot the data for each year in a separate subplot
for i, year in enumerate(range(2018, 2024)):
    ax = axes[i]
    ax.scatter(activities_daily.loc[f'{year}', :].index, activities_daily.loc[f'{year}', 'Relative Effort'], s=2)
    ax.plot(activities_daily.loc[f'{year}', :].index, activities_daily.loc[f'{year}', '14-day Moving Average'], color='red', label='14-day Moving Average')
    ax.plot(activities_daily.loc[f'{year}', :].index, activities_daily.loc[f'{year}', '30-day Moving Average'], color='pink', label='30-day Moving Average')
    ax.set_title(f'{year}')
    ax.set_ylabel('Relative Effort')
    ax.set_ylim([0,100]) 

    # Set the x-axis label format and ticks
    ax.xaxis.set_major_formatter(date_fmt)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.set_xlim([pd.to_datetime(f'{year}-01-01'), pd.to_datetime(f'{year}-12-31')])
    ax.set_xticks(pd.date_range(start=pd.to_datetime(f'{year}-01-01'), end=pd.to_datetime(f'{year}-12-31'), freq='MS'))
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    
# Add x-axis label to bottom subplot
axes[-1].set_xlabel('Month')

# Set the figure title
fig.suptitle('Daily Relative Effort by Year', fontsize=16, fontweight='bold', y=1.0)

# Add a single legend to the bottom of the figure
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=2, fontsize='medium')

# Adjust spacing between subplots 
fig.subplots_adjust(hspace=0.65, top=0.95, bottom=0.1)

plt.show()

# save as PNG
fig.savefig('myplot.png', dpi=300, bbox_inches='tight')
