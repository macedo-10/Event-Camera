import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze the oscillation periods of a pixel from event data.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--x', type=int, required=True, help='X coordinate of the pixel.')
    parser.add_argument('--y', type=int, required=True, help='Y coordinate of the pixel.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    return parser.parse_args()

def analyze_oscillation_periods(input_csv, x, y, t_min=None, t_max=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Filter the DataFrame for the specified pixel
    pixel_df = df[(df['x'] == x) & (df['y'] == y)].sort_values(by='t')

    if t_min is not None:
        pixel_df = pixel_df[pixel_df['t'] >= t_min]
    if t_max is not None:
        pixel_df = pixel_df[pixel_df['t'] <= t_max]

    if pixel_df.empty:
        print(f"No data found for pixel ({x}, {y}) within the specified time range.")
        return

    # Extract time and polarity
    time = pixel_df['t'].values
    polarity = pixel_df['p'].values

    # Detect polarity changes (extrema)
    changes = np.where(np.diff(polarity) != 0)[0] + 1

    # Calculate time intervals between changes to find oscillation periods
    periods = np.diff(time[changes])

    # Plot the polarity over time with detected changes
    plt.figure(figsize=(10, 6))
    plt.plot(time, polarity, label='Polarity')
    plt.plot(time[changes], polarity[changes], 'rx', label='Polarity Changes')
    plt.xlabel('Time (t)')
    plt.ylabel('Polarity (p)')
    plt.title(f'Polarity of Pixel ({x}, {y}) Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print periods between polarity changes
    print("Oscillation periods between polarity changes:")
    for i, period in enumerate(periods):
        print(f"Cycle {i+1}: {period} time units")

def main():
    args = parse_args()
    analyze_oscillation_periods(args.input_csv, args.x, args.y, args.tmin, args.tmax)

if __name__ == "__main__":
    main()
