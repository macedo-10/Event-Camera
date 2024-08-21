import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Plot a histogram of the number of events over time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('--polarity', type=int, choices=[0, 1], help='Filter events by polarity: 0 for negative, 1 for positive.')
    return parser.parse_args()

def plot_event_histogram(input_csv, xmin, xmax, ymin, ymax, tmin=None, tmax=None, polarity=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Apply time filtering if specified
    if tmin is not None:
        df = df[df['t'] >= tmin]
    if tmax is not None:
        df = df[df['t'] <= tmax]

    # Apply polarity filtering if specified
    if polarity is not None:
        df = df[df['p'] == polarity]

    # Filter the DataFrame based on the specified x and y range
    df = df[(df['x'] >= xmin) & (df['x'] <= xmax) & (df['y'] >= ymin) & (df['y'] <= ymax)]

    # Create bins for time values
    time_bins = np.linspace(df['t'].min(), df['t'].max(), num=100)

    # Create a histogram
    plt.figure(figsize=(10, 8))
    plt.hist(df['t'], bins=time_bins, color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel('Time (t) us')
    plt.ylabel('Number of events')
    plt.title('Histogram of Number of Events over Time')
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_event_histogram(args.input_csv, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
