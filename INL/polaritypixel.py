import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the polarity of a single pixel over time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('-x', '--x-coordinate', type=int, required=True, help='X coordinate of the pixel.')
    parser.add_argument('-y', '--y-coordinate', type=int, required=True, help='Y coordinate of the pixel.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    return parser.parse_args()

def plot_pixel_polarity(input_csv, x, y, tmin=None, tmax=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Filter the DataFrame for the specified pixel
    pixel_df = df[(df['x'] == x) & (df['y'] == y)]

    # Apply time filtering if specified
    if tmin is not None:
        pixel_df = pixel_df[pixel_df['t'] >= tmin]
    if tmax is not None:
        pixel_df = pixel_df[pixel_df['t'] <= tmax]

    # Plot the polarity over time
    plt.figure(figsize=(10, 6))
    plt.scatter(pixel_df['t'], pixel_df['p'], c=pixel_df['p'], cmap='bwr', marker='.')
    plt.colorbar(label='Polarity')
    plt.xlabel('Time (t)')
    plt.ylabel('Polarity (p)')
    plt.title(f'Polarity of Pixel ({x}, {y}) Over Time')
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_pixel_polarity(args.input_csv, args.x_coordinate, args.y_coordinate, args.tmin, args.tmax)

if __name__ == "__main__":
    main()
