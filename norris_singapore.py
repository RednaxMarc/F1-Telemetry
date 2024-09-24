import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Get the XML content
url = "http://ergast.com/api/f1/2024/last/drivers/norris/laps.xml?limit=62"
response = requests.get(url)
root = ET.fromstring(response.content)

# Handle namespaces
ns = {'mrd': 'http://ergast.com/mrd/1.5'}

# Get the lap times
lap_times = [lap.find('.//mrd:Timing',ns).attrib['time'] for lap in root.findall('.//mrd:Lap',ns)]

# Function to convert lap time from 'MM:SS.mmm' to total seconds
def lap_time_to_seconds(lap_time):
    minutes, seconds = lap_time.split(':')
    return int(minutes) * 60 + float(seconds)

# Convert all lap times to seconds
lap_times_in_seconds = [lap_time_to_seconds(lap_time) for lap_time in lap_times]

# Generate lap numbers (1, 2, 3, ...)
lap_numbers = list(range(1, len(lap_times_in_seconds) + 1))

# Get the lap where Lando pitted, and remove that lap from the lap times
url = 'http://ergast.com/api/f1/2024/last/drivers/norris/pitstops.xml'
response = requests.get(url)
root = ET.fromstring(response.content)
pit_laps = [int(pit_lap.find('.//mrd:PitStop', ns).attrib['lap']) for pit_lap in root.findall('.//mrd:PitStopsList', ns)]
print(pit_laps)
for i in pit_laps:
    lap_times_in_seconds.pop(i-1)
    lap_numbers.pop(i-1)
print(len(lap_times_in_seconds))
print(len(lap_numbers))


# Plotting the lap times
plt.plot(lap_numbers, lap_times_in_seconds, marker='o', linestyle='-', color='b')

# Adding labels and title
plt.title('Lap Times Over Race', fontsize=14)
plt.xlabel('Lap Number', fontsize=12)
plt.ylabel('Lap Time (seconds)', fontsize=12)

# Show the plot
plt.grid(True)
plt.show()

# Make a boxplot of the lap times
plt.boxplot(lap_times_in_seconds)
plt.title('Lap Times Boxplot', fontsize=14)
plt.ylabel('Lap Time (seconds)', fontsize=12)
plt.show()



