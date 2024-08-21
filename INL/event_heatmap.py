import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import matplotlib.colors as mcolors

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the number of events per pixel in a heatmap.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--xmin', type=int, required=False, default=None, help='Minimum x value to consider.')
    parser.add_argument('--xmax', type=int, required=False, default=None, help='Maximum x value to consider.')
    parser.add_argument('--ymin', type=int, required=False, default=None, help='Minimum y value to consider.')
    parser.add_argument('--ymax', type=int, required=False, default=None, help='Maximum y value to consider.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time value to consider.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time value to consider.')
    return parser.parse_args()

def plot_event_counts(input_csv, xmin=None, xmax=None, ymin=None, ymax=None, tmin=None, tmax=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])
    
    print("Initial data read from CSV:")
    print(df.head())
    
    # Apply filtering based on x, y, and t if specified
    if xmin is not None:
        df = df[df['x'] >= xmin]
    if xmax is not None:
        df = df[df['x'] <= xmax]
    if ymin is not None:
        df = df[df['y'] >= ymin]
    if ymax is not None:
        df = df[df['y'] <= ymax]
    if tmin is not None:
        df = df[df['t'] >= tmin]
    if tmax is not None:
        df = df[df['t'] <= tmax]
    
    print("Data after filtering:")
    print(df.head())
    print(f"Number of events after filtering: {len(df)}")

    # Count the number of events per pixel
    event_counts = df.groupby(['x', 'y']).size().reset_index(name='counts')
    
    print("Event counts per pixel:")
    print(event_counts.head())
    
    # Create a pivot table to have a 2D representation of the event counts
    event_counts_pivot = event_counts.pivot(index='y', columns='x', values='counts').fillna(0).astype(int)
    
    print("Event counts pivot table:")
    print(event_counts_pivot.head())

    # Plot the heatmap with a logarithmic color scale
    plt.figure(figsize=(10, 8))
    min_nonzero = event_counts_pivot[event_counts_pivot > 0].min().min()
    norm = mcolors.LogNorm(vmin=min_nonzero, vmax=event_counts_pivot.values.max())
    plt.imshow(event_counts_pivot, cmap='viridis', origin='lower', aspect='auto', norm=norm)
    plt.colorbar(label='Number of events per pixel (log scale)')
    plt.xlabel('x [px]')
    plt.ylabel('y [px]')
    plt.title('Event counts per pixel')
    plt.show()

def main():
    args = parse_args()
    plot_event_counts(args.input_csv, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax)

if __name__ == "__main__":
    main()
