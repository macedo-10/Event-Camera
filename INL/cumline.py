import pandas as pd
import matplotlib.pyplot as plt
import argparse
from sklearn.linear_model import LinearRegression
import numpy as np
import scipy

def parse_args():
    parser = argparse.ArgumentParser(description='Plot the cumulative polarity of a horizontal line of pixels over time and optionally find slopes.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum X coordinate of the horizontal line of pixels.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum X coordinate of the horizontal line of pixels.')
    parser.add_argument('-y', '--y-coordinate', type=int, required=True, help='Y coordinate of the horizontal line of pixels.')
    parser.add_argument('--tmin', type=int, required=False, default=None, help='Minimum time threshold.')
    parser.add_argument('--tmax', type=int, required=False, default=None, help='Maximum time threshold.')
    parser.add_argument('-s', '--slope', action='store_true', help='Flag to indicate if slope calculation is needed.')
    return parser.parse_args()

def plot_cumulative_polarity_and_find_slopes(input_csv, xmin, xmax, y, tmin=None, tmax=None, calculate_slope=False):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Filter the DataFrame for the specified horizontal line of pixels
    line_df = df[(df['y'] == y) & (df['x'] >= xmin) & (df['x'] <= xmax)]

    # Apply time filtering if specified
    if tmin is not None:
        line_df = line_df[line_df['t'] >= tmin]
    if tmax is not None:
        line_df = line_df[line_df['t'] <= tmax]

    # Calculate the cumulative sum of polarity (1 for positive, -1 for negative)
    line_df['cumulative_p'] = line_df['p'].apply(lambda p: 1 if p == 1 else -1).cumsum()

    # Plot the cumulative sum over time
    # plt.figure(figsize=(10, 6))

    fig, ax = plt.subplots(2, 1, sharex=True)
    plt.sca(ax[0])
    colors = ["C0", "C1"]
    colors_vec = [colors[p] for p in line_df['p']]
    plt.scatter(line_df['t'], line_df['y'], s=0.5, c=colors_vec)

    plt.sca(ax[1])
    plt.plot(line_df['t'], line_df['cumulative_p'], label=f'Cumulative Polarity for Y = {y}', drawstyle='steps-post')
    detrend = scipy.signal.detrend( line_df['cumulative_p'])
    plt.plot(line_df['t'], detrend)

    if calculate_slope:
        # Define the segments for regression manually
        regression_segments = [
            (1000000, 1560000),
            (1560000, 1720000),
            (1720000, 2560000),
            (2562250, 2635500),
            (2640000, 3000000)
            # Add more segments here as needed
        ]

        slopes = []
        for i, (start, end) in enumerate(regression_segments):
            segment = line_df[(line_df['t'] >= start) & (line_df['t'] < end)]
            if len(segment) > 1:
                X = segment['t'].values.reshape(-1, 1)
                y = segment['cumulative_p'].values
                model = LinearRegression().fit(X, y)
                slope = model.coef_[0]
                slopes.append(slope)
                #plt.plot(segment['t'], model.predict(X), label=f'Segment {i+1} Slope: {slope:.2f}')
            else:
                slopes.append(None)
                print(f"Not enough data points for segment {i+1} ({start}-{end})")

        print(f"Slopes of the segments: {slopes}")

    plt.xlabel('Time (t)')
    plt.ylabel('Cumulative Polarity')
    plt.title(f'Cumulative Polarity of Pixels from ({xmin}, {y}) to ({xmax}, {y}) Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    args = parse_args()
    plot_cumulative_polarity_and_find_slopes(args.input_csv, args.xmin, args.xmax, args.y_coordinate, args.tmin, args.tmax, args.slope)

if __name__ == "__main__":
    main()
