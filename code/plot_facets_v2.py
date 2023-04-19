import os
import gpxpy
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns 

# Specify the folder path containing GPX files
folder_path = r'C:\Users\JessieWilson\Queries\strava\activities_gpx'

# Initialize an empty list to store GPX data
gpx_data = []

# Loop through each GPX file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.gpx'):  # Filter for GPX files
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            # Extract relevant data from the GPX file and append to the list
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        if point.time.year > 2017:  # Add a condition to filter by year
                            gpx_data.append({
                                'lat': point.latitude,
                                'lon': point.longitude,
                                'time': point.time,
                                'name': track.name,  # Add 'name' from GPX track
                                'ele': getattr(point, 'ele', None), # Use getattr to handle missing 'ele' attribute                                
                                'dist': getattr(track, 'dist', None)  # Use getattr to handle missing 'dist' attribute
                                # Add other relevant data as needed
                            })

# Create a DataFrame from the list of dictionaries containing GPX data
df = pd.DataFrame(gpx_data)

# Print the head of the DataFrame (default: first 5 rows)
# print(df.head()


def plot_facets(df, output_file = 'plot.png'):

    # Create a new figure
    plt.figure()

    # Compute activity start times (for facet ordering)
    start_times = df.groupby('name').agg({'time': 'min'}).reset_index().sort_values('time')
    ncol = math.ceil(math.sqrt(len(start_times)))
    
    # Create facets
    p = sns.FacetGrid(
        data = df,
        col = 'name',
        col_wrap = ncol,
        col_order = start_times['name'],
        sharex = False,
        sharey = False,
        )

    # Add activities
    p = p.map(
        plt.plot, "lon", "lat", color = 'black', linewidth = 4
        )

    # Update plot aesthetics
    p.set(xlabel = None)
    p.set(ylabel = None)
    p.set(xticks = [])
    p.set(yticks = [])
    p.set(xticklabels = [])
    p.set(yticklabels = [])
    p.set_titles(col_template = '', row_template = '')
    sns.despine(left = True, bottom = True)
    plt.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.95, top = 0.95)
    plt.savefig(output_file)


plot_facets(df, output_file = 'facet_plot.png')
