import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

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

def process_chunk(chunk, xmin, xmax, ymin, ymax, tmin, tmax, polarity):
    # Apply time filtering if specified
    if tmin is not None:
        chunk = chunk[chunk['t'] >= tmin]
    if tmax is not None:
        chunk = chunk[chunk['t'] <= tmax]

    # Apply polarity filtering if specified
    if polarity is not None:
        chunk = chunk[chunk['p'] == polarity]

    # Filter the DataFrame based on the specified x and y range
    chunk = chunk[(chunk['x'] >= xmin) & (chunk['x'] <= xmax) & (chunk['y'] >= ymin) & (chunk['y'] <= ymax)]

    return chunk

def plot_lines_polarity_over_time(input_csv, xmin, xmax, ymin, ymax, tmin=None, tmax=None, polarity=None):
    chunk_size = 1000000  # Adjust chunk size based on your system's memory
    chunks = []
    
    # Read the CSV file in chunks
    for chunk in pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'], chunksize=chunk_size):
        chunk = process_chunk(chunk, xmin, xmax, ymin, ymax, tmin, tmax, polarity)
        chunks.append(chunk)

    # Concatenate all processed chunks
    df = pd.concat(chunks, ignore_index=True)

    # Debug: Print the first few rows after filtering
    print("Filtered data:")
    print(df.head())

    # Check if the filtered DataFrame is empty
    if df.empty:
        print("No events found for the given filters.")
        return

    # Reset DataFrame index
    df.reset_index(drop=True, inplace=True)

    # Create bins for time and y values
    time_bins = np.linspace(df['t'].min(), df['t'].max(), num=500)
    y_bins = np.arange(ymin, ymax + 1)

    # Create a 2D histogram for density calculation
    heatmap, xedges, yedges = np.histogram2d(df['t'], df['y'], bins=[time_bins, y_bins])

    # Flatten the heatmap to get a list of densities
    densities = heatmap.T.flatten()
    densities = densities / densities.max() if densities.max() != 0 else densities  # Normalize densities

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

        # Debugging information inside the loop
        print(f"Processing y={y}")
        print(f"Line df indices (first 10): {line_indices[:10]}")
        print(f"Valid density indices (first 10): {valid_indices[:10]}")

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

def main():
    args = parse_args()
    plot_lines_polarity_over_time(args.input_csv, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
