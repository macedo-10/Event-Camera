import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the polarity of multiple vertical lines of pixels over time.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum Y coordinate of the vertical lines of pixels.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum Y coordinate of the vertical lines of pixels.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the vertical lines of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the vertical lines of pixels.')
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

    # Plot the polarities over time, shifting each line's plot to the right
    plt.figure(figsize=(10, 6))
    for idx, x in enumerate(range(xmin, xmax + 1)):
        line_df = df[(df['x'] == x) & (df['y'] >= ymin) & (df['y'] <= ymax)]
        plt.scatter(line_df['t'], line_df['p'] + idx * 2, label=f'Line at x={x}', s=10)

    plt.xlabel('Time (t)')
    plt.ylabel('Shifted Polarity (p)')
    plt.title(f'Polarities of Vertical Lines from x={xmin} to x={xmax} Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_lines_polarity_over_time(args.input_csv, args.xmin, args.xmax, args.ymin, args.ymax, args.tmin, args.tmax, args.polarity)

if __name__ == "__main__":
    main()
