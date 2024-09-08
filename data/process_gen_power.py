import pandas as pd
import matplotlib.pyplot as plt

'''
source data
https://www.eia.gov/electricity/gridmonitor/dashboard/custom/pending

'''
# Define the investment values (these should be defined according to your context)
WND_PPA_MW = 3  # Example investment value for wind, replace with actual value
SUN_PPA_MW = 1.9  # Example investment value for solar, replace with actual value

# Load the data from a CSV file
filename = "cal-pacific-time"
data = pd.read_csv(filename + ".csv")

# Convert negative values to zero
data['Wind Generation (MWh)'] = data['Wind Generation (MWh)'].clip(lower=0)
data['Solar Generation (MWh)'] = data['Solar Generation (MWh)'].clip(lower=0)

# Calculate the maximum capacities
max_wnd_cap = data['Wind Generation (MWh)'].max()
max_sun_cap = data['Solar Generation (MWh)'].max()

# Normalize the wind and solar generation based on the investments and maximum capacities
data['WND'] = data['Wind Generation (MWh)'] / max_wnd_cap * WND_PPA_MW
data['SUN'] = data['Solar Generation (MWh)'] / max_sun_cap * SUN_PPA_MW

# Create the hour index
data['hour_index'] = range(len(data))

# Select only the required columns
result = data[['hour_index', 'WND', 'SUN']]

# Print the result
print(result.to_csv(index=False))

# You can save the result to a CSV file if needed
result.to_csv(filename + '_processed.csv', index=False)

# Plotting the stacked area chart
plt.figure(figsize=(10, 6))
plt.stackplot(result['hour_index'], result['WND'], result['SUN'], labels=['Wind', 'Solar'], colors=['#87CEEB', '#FFD700'])
plt.xlabel('Hour Index')
plt.ylabel('Normalized Generation (MW)')
plt.title('Wind and Solar Power Generation')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()
