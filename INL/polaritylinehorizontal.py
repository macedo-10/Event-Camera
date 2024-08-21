import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the polarity of a horizontal line of pixels over time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the horizontal line of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the horizontal line of pixels.')
    parser.add_argument('-y', '--y-coordinate', type=int, required=True, help='Y coordinate of the horizontal line of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('--polarity', type=int, choices=[0, 1], required=False, default=None, help='Polarity to filter (0 for negative, 1 for positive).')
    return parser.parse_args()

def plot_horizontal_line_polarity(input_csv, xmin, xmax, y, tmin=None, tmax=None, polarity=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Filter the DataFrame for the specified horizontal line of pixels
    line_df = df[(df['y'] == y) & (df['x'] >= xmin) & (df['x'] <= xmax)]

    # Apply time filtering if specified
    if tmin is not None:
        line_df = line_df[line_df['t'] >= tmin]
    if tmax is not None:
        line_df = line_df[line_df['t'] <= tmax]

    # Apply polarity filtering if specified
    if polarity is not None:
        line_df = line_df[line_df['p'] == polarity]

    # Plot the polarities over time, shifting each pixel's plot upwards
    plt.figure(figsize=(10, 6))
    for idx, x in enumerate(range(xmin, xmax + 1)):
        pixel_df = line_df[line_df['x'] == x]
        plt.scatter(pixel_df['t'], pixel_df['p'] + idx * 2, label=f'Pixel ({x}, {y})', s=10)

    plt.xlabel('Time (t)')
    plt.ylabel('Shifted Polarity (p)')
    plt.title(f'Polarities of Pixels from ({xmin}, {y}) to ({xmax}, {y}) Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_horizontal_line_polarity(args.input_csv, args.xmin, args.xmax, args.y_coordinate, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
