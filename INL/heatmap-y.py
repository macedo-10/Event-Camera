import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Plot a heatmap of Y values as a function of Time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('--polarity', type=int, choices=[0, 1], help='Filter events by polarity: 0 for negative, 1 for positive.')
    return parser.parse_args()

def plot_heatmap(input_csv, xmin, xmax, ymin, ymax, tmin=None, tmax=None, polarity=None):
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

    # Create bins for time and y values
    time_bins = np.linspace(df['t'].min(), df['t'].max(), num=1000)
    y_bins = np.arange(ymin, ymax + 1)

    # Create a 2D histogram
    heatmap, xedges, yedges = np.histogram2d(df['t'], df['y'], bins=[time_bins, y_bins])

    # Apply logarithmic scale to the heatmap
    heatmap = np.log1p(heatmap)  # Use log1p to avoid log(0)

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap.T, origin='lower', aspect='auto', extent=[time_bins[0], time_bins[-1], ymin, ymax], cmap='viridis')
    plt.colorbar(label='Log of Number of events')
    plt.xlabel('Time (t) us')
    plt.ylabel('Y coordinate')
    plt.title('Heatmap of Y values as a function of Time (Log Scale)')
    plt.show()

def main():
    args = parse_args()
    plot_heatmap(args.input_csv, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
