import matplotlib.pyplot as plt
import pandas as pd
import sys

FILE_NAME = sys.argv[1]


def main():
    """
    Main function to read RTT data from a CSV file, plot the RTT and Smoothed RTT values,
    and save the plot as a PNG file.

    The CSV file should be located in the 'CSV' directory and should be named 'RTTs_<FILE_NAME>.csv'.
    The output plot will be saved in the 'plots' directory with the name 'RTTs_<FILE_NAME>.png'.
    """

    # Load the CSV data
    rtt_csv = pd.read_csv(f"CSV/RTTs_{FILE_NAME}.csv")

    # Set up the plot
    plt.figure(figsize=(10, 6))
    plt.plot(rtt_csv['RTT'], color='blue', label='RTT')
    plt.plot(rtt_csv['Smoothed RTT'], color='red', label='Smoothed RTT')

    # Add labels and title
    plt.xlabel('Packets')
    plt.ylabel('RTT value')
    plt.title('RTT across time - ' + FILE_NAME)

    # Add legend
    plt.legend()

    # Save the plot as a PNG file
    plt.savefig(f'plots/RTTs_{FILE_NAME}.png')


if __name__ == '__main__':
    main()
