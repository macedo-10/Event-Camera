import os
import shutil
import time
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from metavision_core.event_io import EventsIterator

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Monitor directory for new RAW files, convert to CSV and plot polarities over time.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the horizontal lines of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('--polarity', type=int, choices=[0, 1], help='Filter events by polarity: 0 for negative, 1 for positive.')
    args = parser.parse_args()
    return args

def convert_raw_to_csv(event_file_path, start_ts=0, max_duration=1e6*60, delta_t=1000000):
    if os.path.isfile(event_file_path):
        output_file = event_file_path.replace('.raw', '.csv')
    else:
        raise TypeError(f'Fail to access file: {event_file_path}')

    if os.path.exists(output_file):
        print(f"CSV file {output_file} already exists. Skipping conversion.")
        return output_file

    mv_iterator = EventsIterator(input_path=event_file_path, delta_t=delta_t, start_ts=start_ts, max_duration=max_duration)

    with open(output_file, 'w') as csv_file:
        for evs in tqdm(mv_iterator, total=max_duration // delta_t):
            for (x, y, p, t) in evs:
                csv_file.write("%d,%d,%d,%d\n" % (x, y, p, t))

    print(f"Conversion completed: {output_file}")
    return output_file

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

    # Filter the DataFrame based on the specified x and y range
    df = df[(df['x'] >= xmin) & (df['x'] <= xmax) & (df['y'] >= ymin) & (df['y'] <= ymax)]

    # Reset DataFrame index
    df.reset_index(drop=True, inplace=True)

    # Create bins for time and y values
    time_bins = np.linspace(df['t'].min(), df['t'].max(), num=500)
    y_bins = np.arange(ymin, ymax + 1)

    # Create a 2D histogram for density calculation
    heatmap, xedges, yedges = np.histogram2d(df['t'], df['y'], bins=[time_bins, y_bins])

    # Flatten the heatmap to get a list of densities
    densities = heatmap.T.flatten()
    densities = densities / densities.max()  # Normalize densities

    # Ensure the index calculation fits within the density array bounds
    time_indices = np.digitize(df['t'], bins=time_bins) - 1
    y_indices = np.digitize(df['y'], bins=y_bins) - 1

    # Clip the indices to ensure they are within bounds
    time_indices = np.clip(time_indices, 0, heatmap.shape[1] - 1)
    y_indices = np.clip(y_indices, 0, heatmap.shape[0] - 1)

    # Create a valid density index for each event
    density_indices = np.ravel_multi_index((y_indices, time_indices), heatmap.shape)
    density_indices = np.clip(density_indices, 0, densities.size - 1)  # Ensure all indices are within bounds

    # Debugging information
    print(f"Number of events: {len(df)}")
    print(f"Density array shape: {densities.shape}")
    print(f"Density indices shape: {density_indices.shape}")
    print(f"Max density index: {density_indices.max()}")
    print(f"Min density index: {density_indices.min()}")
    print(f"Densities size: {densities.size}")
    print(f"Density indices (first 10): {density_indices[:10]}")

    # Plot the polarities over time with point sizes based on density
    plt.figure(figsize=(10, 6))
    colors = ["C0", "C1"]
    for y in range(ymax, ymin - 1, -1):
        line_df = df[df['y'] == y]
        if len(line_df) == 0:
            continue

        # Adjust indices to ensure they are within bounds
        line_indices = line_df.index.to_numpy()
        valid_indices = density_indices[line_indices]


        # Clip valid_indices to avoid out-of-bounds error
        valid_indices = np.clip(valid_indices, 0, densities.size - 1)
        point_sizes = np.clip(densities[valid_indices], 0.05, 5)  # Smaller point sizes
        colors_vec = [colors[p] for p in line_df['p']]
        plt.scatter(line_df['t'], line_df['y'], s=point_sizes, c=colors_vec)

    plt.xlabel('Time (t)')
    plt.ylabel('Y coordinate')
    plt.title(f'Polarities of Horizontal Lines from y={ymin} to y={ymax} Over Time')
    plt.grid(True)
    plt.show()

def monitor_directory(source_dir, dest_dir, xmin, xmax, ymin, ymax, tmin=None, tmax=None, polarity=None):
    processed_files = set()
    while True:
        raw_files = [f for f in os.listdir(source_dir) if f.endswith('.raw') and f not in processed_files]
        for raw_file in raw_files:
            source_path = os.path.join(source_dir, raw_file)
            dest_path = os.path.join(dest_dir, raw_file)
            shutil.copy(source_path, dest_path)
            print(f"Copied {source_path} to {dest_path}")

            csv_file = convert_raw_to_csv(dest_path)
            plot_lines_polarity_over_time(csv_file, xmin, xmax, ymin, ymax, tmin, tmax, polarity)

            processed_files.add(raw_file)
        time.sleep(10)

def main():
    args = parse_args()
    source_dir = r"C:\Users\Pedro\Documents\metavision\recordings"
    dest_dir = r"C:\Users\Pedro\Desktop\INL"
    monitor_directory(source_dir, dest_dir, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
