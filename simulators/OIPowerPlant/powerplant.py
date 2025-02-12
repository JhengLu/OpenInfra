import random
import pandas as pd

class PowerGenerator:
    def __init__(self, location="cal", time_zone = "pacific-time"):
        self.generated_power = 0
        self.location = location
        self.time_zone = time_zone
        self.power_raw_trace_df = pd.read_csv(f"/app/data/{self.location}-{self.time_zone}.csv", index_col=0)
        self.power_projected_trace_df = self.project_power_trace()
        self.power_projected_trace_df.to_csv(f"/app/data/{self.location}-{self.time_zone}-processed.csv")



    def generate_power(self, time_step):
        return (self.power_projected_trace_df.loc[time_step, 'WND'] + self.power_projected_trace_df.loc[time_step, 'SUN']) * 1000000, self.power_projected_trace_df.loc[time_step, 'WND'] * 1000000, self.power_projected_trace_df.loc[time_step, 'SUN'] * 1000000 # translate MW to W


    def project_power_trace(self):
        # Define the investment values (these should be defined according to your context)
        WND_PPA_MW = 3  # Example investment value for wind, replace with actual value
        SUN_PPA_MW = 1.9  # Example investment value for solar, replace with actual value

        # Load the data from a CSV file
        filename = "data/cal-pacific-time"
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

        return result


