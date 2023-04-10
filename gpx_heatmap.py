import os
import gpxpy
import folium
from folium.plugins import HeatMap

# Step 1: Parse GPX files
# Specify the directory containing the GPX files
gpx_directory = r"<path\to\file>"  # Update with the correct path to the directory containing the GPX files

# Create an empty list to store the extracted route data
route_data = []

for gpx_file in os.listdir(gpx_directory):
    if gpx_file.endswith('.gpx'):
        with open(os.path.join(gpx_directory, gpx_file), 'r', encoding='utf-8') as f:  # Specify encoding
            gpx = gpxpy.parse(f)
            for track in gpx.tracks:
                for segment in track.segments:
                    # Extract latitude and longitude coordinates of each point in the segment
                    segment_data = [(point.latitude, point.longitude) for point in segment.points]
                    # Append segment data to route data
                    route_data.append(segment_data)

# Step 2: Create HeatMap
# Create a folium map centered on the first point of the first segment
m = folium.Map(location=route_data[0][0], zoom_start=13)

# Create a HeatMap layer with the route data
heat_data = []
for segment_data in route_data:
    heat_data += segment_data

heat_map = HeatMap(heat_data, radius=11, blur=8)  # Adjust radius and blur parameters as desired
heat_map.add_to(m)

# Step 3: Add Line Map
# Loop through the route data and add a PolyLine layer for each segment
for segment_data in route_data:
    folium.PolyLine(segment_data, color='blue', weight=2.5, opacity=1).add_to(m)

# Step 4: Customize maps (optional)
# You can customize the map by adding markers, changing colors, etc.

# Step 5: Export maps
# Save the map as an HTML file
m.save('heatmap_with_line_map.html')
