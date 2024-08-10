import matplotlib.pyplot as plt
import pandas as pd

def plot_power_usage(csv_file):
    data = pd.read_csv(csv_file)

    # Determine the number of UPS units in the data
    num_ups = len([col for col in data.columns if 'UPS' in col and 'Status' in col])

    # Calculate the total UPS deliverable power
    data['Total UPS Deliverable Power'] = 0
    for ups_id in range(1, num_ups + 1):
        status_col = f'UPS {ups_id} Status'
        power_col = f'UPS {ups_id} Deliverable Power'
        data['Total UPS Deliverable Power'] += data[power_col] * data[status_col]

    # Create a figure with two rows and two columns of subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Plot power usage in the first subplot with stacked Wind and Solar Power
    axs[0, 0].plot(data['Time'], data['Total Power Usage'], label='Total Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Server Power Usage'], label='Server Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Cool Power Usage'], label='Cool Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Other Power Usage'], label='Other Power Usage', linestyle='-', linewidth=1)
    axs[0, 0].plot(data['Time'], data['Total UPS Deliverable Power'], label='Total UPS Deliverable Power', linestyle='-', linewidth=2, color='k')

    # Add stacked area plots for Wind and Solar Power
    axs[0, 0].stackplot(data['Time'], data['Wind Power'], data['Solar Power'], labels=['Wind Power', 'Solar Power'], alpha=0.5)

    axs[0, 0].set_xlabel('Time (hours)')
    axs[0, 0].set_ylabel('Power (W)')
    axs[0, 0].set_title('Power Usage Over Time')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Generate line styles for the UPS plots
    linestyles = ['-', '--', '-.', ':']  # Base linestyles
    for ups_id in range(1, num_ups + 1):
        status_col = f'UPS {ups_id} Status'
        battery_col = f'UPS {ups_id} Battery Charge Level'
        online_mask = data[status_col].astype(bool)
        linestyle = linestyles[(ups_id - 1) % len(linestyles)]  # Cycle through linestyles
        axs[0, 1].plot(data['Time'][online_mask], data[battery_col][online_mask], label=battery_col, linestyle=linestyle, linewidth=2)

    axs[0, 1].axhline(y=data['Battery Control Limit'].iloc[0], color='r', linestyle='--', label='Battery Control Limit')
    axs[0, 1].axhline(y=data['Battery Recover Signal'].iloc[0], color='g', linestyle='--', label='Battery Recover Signal')

    axs[0, 1].set_xlabel('Time (hours)')
    axs[0, 1].set_ylabel('Charge Level (Wh)')
    axs[0, 1].set_title('Battery Charge Level Over Time')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot rack max load percentage in the third subplot
    for col in [col for col in data.columns if 'Max Load %' in col]:
        axs[1, 0].plot(data['Time'], data[col], label=col, linewidth=2)

    axs[1, 0].set_xlabel('Time (hours)')
    axs[1, 0].set_ylabel('Max Load Percentage (%)')
    axs[1, 0].set_title('Rack Max Load Percentage Over Time')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Plot UPS deliverable power in the fourth subplot
    for ups_id in range(1, num_ups + 1):
        status_col = f'UPS {ups_id} Status'
        power_col = f'UPS {ups_id} Deliverable Power'
        online_mask = data[status_col].astype(bool)
        linestyle = linestyles[(ups_id - 1) % len(linestyles)]  # Cycle through linestyles
        axs[1, 1].plot(data['Time'][online_mask], data[power_col][online_mask], label=power_col, linestyle=linestyle, linewidth=2)

    axs[1, 1].set_xlabel('Time (hours)')
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
