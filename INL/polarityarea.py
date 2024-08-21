import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the polarity of multiple horizontal lines of pixels over time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('--polarity', type=int, choices=[0, 1], help='Filter events by polarity: 0 for negative, 1 for positive.')
    return parser.parse_args()

def plot_lines_polarity_over_time(input_csv, xmin, xmax, ymin, ymax, tmin=None, tmax=None, polarity=None):
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

    colors = ["C0", "C1"]
    # Plot the polarities over time, shifting each line's plot downwards
    plt.figure(figsize=(10, 6))
    for idx, y in enumerate(range(ymax, ymin - 1, -1)):
        line_df = df[(df['y'] == y) & (df['x'] >= xmin) & (df['x'] <= xmax)]
        colors_vec = [colors[p] for p in line_df['p']]
        plt.scatter(line_df['t'], line_df['y'], s=0.01, c=colors_vec)  # Adjusted size of the points to be smaller (parameter s)

    plt.xlabel('Time (t)')
    plt.ylabel('Y coordinate')
    plt.title(f'Polarities of Horizontal Lines from y={ymin} to y={ymax} Over Time')
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_lines_polarity_over_time(args.input_csv, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()