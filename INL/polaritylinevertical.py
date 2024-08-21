import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the polarity of a vertical line of pixels over time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('-x', '--x-coordinate', type=int, required=True, help='X coordinate of the vertical line of pixels.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the vertical line of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the vertical line of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('--polarity', type=int, choices=[0, 1], required=False, default=None, help='Polarity to filter (0 for negative, 1 for positive).')
    return parser.parse_args()

def plot_vertical_line_polarity(input_csv, x, ymin, ymax, tmin=None, tmax=None, polarity=None):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Filter the DataFrame for the specified vertical line of pixels
    line_df = df[(df['x'] == x) & (df['y'] >= ymin) & (df['y'] <= ymax)]

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
    for idx, y in enumerate(range(ymin, ymax + 1)):
        pixel_df = line_df[line_df['y'] == y]
        plt.scatter(pixel_df['t'], pixel_df['p'] + idx * 2, label=f'Pixel ({x}, {y})', s=10)

    plt.xlabel('Time (t)')
    plt.ylabel('Shifted Polarity (p)')
    plt.title(f'Polarities of Pixels from ({x}, {ymin}) to ({x}, {ymax}) Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_vertical_line_polarity(args.input_csv, args.x_coordinate, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
