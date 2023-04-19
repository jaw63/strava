import calmap
import matplotlib.pyplot as plt
import pandas as pd

activities = pd.read_csv('activities.csv')

year_min=2020
year_max=2023 
max_dist=200

# Create a new figure
plt.figure()
    
# Process data
activities['Activity Date'] = pd.to_datetime(activities['Activity Date'])
activities['date'] = activities['Activity Date'].dt.date
activities = activities.groupby(['date'])['Distance'].sum()
activities.index = pd.to_datetime(activities.index)
activities.clip(0, max_dist, inplace=True)
    
if year_min:
    activities = activities[activities.index.year>=year_min]
    
if year_max:
    activities = activities[activities.index.year<=year_max]
    
# Create heatmap
fig, ax = calmap.calendarplot(data = activities, daylabels='MTWTFSS',
                dayticks=[0, 2, 4, 6], linewidth=0.5, cmap = 'Blues')
    
# Save plot
fig.set_figheight(8)
fig.set_figwidth(9)
fig.savefig('cal_v2.png', dpi = 600)