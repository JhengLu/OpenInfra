import matplotlib.pyplot as plt
import pandas as pd

def plot_power_usage(csv_file):
    data = pd.read_csv(csv_file)

    # Increase font size and string width
    plt.rcParams.update({
        'font.size': 14,
        'axes.labelsize': 16,
        'axes.titlesize': 18,
        'legend.fontsize': 14,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'lines.linewidth': 2,
        'axes.linewidth': 2
    })

    # Create a figure with two subplots
    fig, axs = plt.subplots(2, 1, figsize=(12, 12))

    # Plot power usage in the first subplot
    axs[0].plot(data['Time'], data['Generated Power'], label='Generated Power')
    axs[0].plot(data['Time'], data['Total Power Usage'], label='Total Power Usage')
    axs[0].plot(data['Time'], data['Server Power Usage'], label='Server Power Usage')
    axs[0].plot(data['Time'], data['Cool Power Usage'], label='Cool Power Usage')
    axs[0].plot(data['Time'], data['Other Power Usage'], label='Other Power Usage')

    axs[0].set_xlabel('Time (seconds)')
    axs[0].set_ylabel('Power (W)')
    axs[0].set_title('Power Usage Over Time')
    axs[0].legend()
    axs[0].grid(True)

    # Plot battery charge level in the second subplot
    axs[1].plot(data['Time'], data['Battery Charge Level'], label='Battery Charge Level')

    axs[1].set_xlabel('Time (seconds)')
    axs[1].set_ylabel('Charge Level (Wh)')
    axs[1].set_title('Battery Charge Level Over Time')
    axs[1].legend()
    axs[1].grid(True)

    # Adjust layout
    plt.tight_layout()
    plt.savefig('power_usage_and_battery_charge_level_plot.pdf')
    plt.show()

if __name__ == "__main__":
    plot_power_usage('power_usage.csv')
