import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the polarity of a vertical line of pixels over time with time bins of 10 us.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('-x', '--x-coordinate', type=int, required=True, help='X coordinate of the vertical line of pixels.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the vertical line of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the vertical line of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    return parser.parse_args()

def plot_polarity_with_time_bins(input_csv, x, ymin, ymax, tmin=None, tmax=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Filter the DataFrame for the specified x-coordinate and y-coordinate range
    line_df = df[(df['x'] == x) & (df['y'] >= ymin) & (df['y'] <= ymax)]

    # Apply time filtering if specified
    if tmin is not None:
        line_df = line_df[line_df['t'] >= tmin]
    if tmax is not None:
        line_df = line_df[line_df['t'] <= tmax]

    # Check if the filtered DataFrame is empty
    if line_df.empty:
        print("No data points found for the given filters.")
        return

    print(f"Number of data points: {len(line_df)}")
    print(f"Time range: {line_df['t'].min()} to {line_df['t'].max()}")

    # Create time bins of 10 microseconds
    time_bins = np.arange(line_df['t'].min(), line_df['t'].max() + 10, 10)
    line_df['time_bin'] = np.digitize(line_df['t'], bins=time_bins) - 1

    # Aggregate polarity data within each time bin
    bin_aggregated_polarity = line_df.groupby('time_bin')['p'].sum().reset_index()
    bin_aggregated_polarity['time'] = time_bins[bin_aggregated_polarity['time_bin']] + 5  # Middle of each 10 us bin

    # Plot the aggregated polarity within each time bin
    plt.figure(figsize=(12, 6))
    plt.scatter(bin_aggregated_polarity['time'], bin_aggregated_polarity['p'], s=10, c='blue', label='Polarity')

    plt.xlabel('Time (t)')
    plt.ylabel('Aggregated Polarity')
    plt.title(f'Aggregated Polarity of Pixels from ({x}, {ymin}) to ({x}, {ymax}) Over Time with 10 us Bins')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_polarity_with_time_bins(args.input_csv, args.x_coordinate, args.ymin, args.ymax, args.tmin, args.tmax)

if __name__ == "__main__":
    main()
