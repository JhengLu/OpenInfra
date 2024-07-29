import matplotlib.pyplot as plt
import pandas as pd

def plot_power_usage(csv_file):
    data = pd.read_csv(csv_file)

    # Create a figure with two rows and two columns of subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Plot power usage in the first subplot (top-left)
    axs[0, 0].plot(data['Time'], data['Generated Power'], label='Generated Power')
    axs[0, 0].plot(data['Time'], data['Total Power Usage'], label='Total Power Usage')
    axs[0, 0].plot(data['Time'], data['Server Power Usage'], label='Server Power Usage')
    axs[0, 0].plot(data['Time'], data['Cool Power Usage'], label='Cool Power Usage')
    axs[0, 0].plot(data['Time'], data['Other Power Usage'], label='Other Power Usage')

    axs[0, 0].set_xlabel('Time (seconds)')
    axs[0, 0].set_ylabel('Power (W)')
    axs[0, 0].set_title('Power Usage Over Time')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot battery charge level in the second subplot (top-right)
    for ups_id in range(1, 4):  # Assuming there are 3 UPS units
        charge_level_col = f'UPS {ups_id} Battery Charge Level'
        status_col = f'UPS {ups_id} Status'
        data_filtered = data[data[status_col] == True]
        axs[0, 1].plot(data_filtered['Time'], data_filtered[charge_level_col], label=charge_level_col)

    # Plot battery control limit and recovery signal lines
    axs[0, 1].plot(data['Time'], data['Battery Control Limit'], linestyle='--', color='red', label='Battery Control Limit')
    axs[0, 1].plot(data['Time'], data['Battery Recover Signal'], linestyle='--', color='green', label='Battery Recover Signal')

    axs[0, 1].set_xlabel('Time (seconds)')
    axs[0, 1].set_ylabel('Charge Level (Wh)')
    axs[0, 1].set_title('Battery Charge Level Over Time')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot rack max load percentages in the third subplot (bottom-left)
    for rack_col in [col for col in data.columns if 'Rack' in col and 'Max Load %' in col]:
        axs[1, 0].plot(data['Time'], data[rack_col], label=rack_col)

    axs[1, 0].set_xlabel('Time (seconds)')
    axs[1, 0].set_ylabel('Max Load Percentage (%)')
    axs[1, 0].set_title('Rack Max Load Percentage Over Time')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Hide the fourth subplot (bottom-right) if not needed
    fig.delaxes(axs[1, 1])

    # Adjust layout
    plt.tight_layout()
    plt.savefig('power_usage_and_battery_charge_level_and_rack_load_plot.pdf')
    plt.show()

if __name__ == "__main__":
    plot_power_usage('power_usage.csv')
