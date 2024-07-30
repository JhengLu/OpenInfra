import matplotlib.pyplot as plt
import pandas as pd

def plot_power_usage(csv_file):
    data = pd.read_csv(csv_file)

    # Create a figure with two rows and two columns of subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Plot power usage in the first subplot
    axs[0, 0].plot(data['Time'], data['Generated Power'], label='Generated Power', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Total Power Usage'], label='Total Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Server Power Usage'], label='Server Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Cool Power Usage'], label='Cool Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Other Power Usage'], label='Other Power Usage', linestyle='-', linewidth=1)

    axs[0, 0].set_xlabel('Time (seconds)')
    axs[0, 0].set_ylabel('Power (W)')
    axs[0, 0].set_title('Power Usage Over Time')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot battery charge level in the second subplot
    for ups_id in range(1, 4):
        status_col = f'UPS {ups_id} Status'
        battery_col = f'UPS {ups_id} Battery Charge Level'
        online_mask = data[status_col].astype(bool)
        axs[0, 1].plot(data['Time'][online_mask], data[battery_col][online_mask], label=battery_col, linestyle=['-', '--', '-.'][ups_id-1], linewidth=2)

    axs[0, 1].axhline(y=data['Battery Control Limit'].iloc[0], color='r', linestyle='--', label='Battery Control Limit')
    axs[0, 1].axhline(y=data['Battery Recover Signal'].iloc[0], color='g', linestyle='--', label='Battery Recover Signal')

    axs[0, 1].set_xlabel('Time (seconds)')
    axs[0, 1].set_ylabel('Charge Level (Wh)')
    axs[0, 1].set_title('Battery Charge Level Over Time')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot rack max load percentage in the third subplot
    axs[1, 0].plot(data['Time'], data['Normal Rack 1 Max Load %'], label='Normal Rack 1 Max Load %', linestyle='-', linewidth=2)
    axs[1, 0].plot(data['Time'], data['Normal Rack 2 Max Load %'], label='Normal Rack 2 Max Load %', linestyle='--', linewidth=2)
    axs[1, 0].plot(data['Time'], data['Normal Rack 3 Max Load %'], label='Normal Rack 3 Max Load %', linestyle='-.', linewidth=2)
    axs[1, 0].plot(data['Time'], data['Wireless Rack 1 Max Load %'], label='Wireless Rack 1 Max Load %', linestyle=':', linewidth=2)

    axs[1, 0].set_xlabel('Time (seconds)')
    axs[1, 0].set_ylabel('Max Load Percentage (%)')
    axs[1, 0].set_title('Rack Max Load Percentage Over Time')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Plot UPS deliverable power in the fourth subplot
    for ups_id in range(1, 4):
        status_col = f'UPS {ups_id} Status'
        power_col = f'UPS {ups_id} Deliverable Power'
        online_mask = data[status_col].astype(bool)
        axs[1, 1].plot(data['Time'][online_mask], data[power_col][online_mask], label=power_col, linestyle=['-', '--', '-.'][ups_id-1], linewidth=2)

    axs[1, 1].set_xlabel('Time (seconds)')
    axs[1, 1].set_ylabel('Power (W)')
    axs[1, 1].set_title('UPS Deliverable Power Over Time')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # Adjust layout
    plt.tight_layout()
    plt.savefig('power_usage_and_battery_charge_level_plot.pdf')
    plt.show()

if __name__ == "__main__":
    plot_power_usage('power_usage.csv')
