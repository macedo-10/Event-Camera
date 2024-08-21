import pandas as pd
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Filter CSV file based on region of interest.')
    parser.add_argument('-i', '--input-csv', required=True, help='Path to input CSV file.')
    parser.add_argument('-o', '--output-csv', required=True, help='Path to save the filtered CSV file.')
    parser.add_argument('--xmin', type=int, required=True, help='Minimum x value of the ROI.')
    parser.add_argument('--xmax', type=int, required=True, help='Maximum x value of the ROI.')
    parser.add_argument('--ymin', type=int, required=True, help='Minimum y value of the ROI.')
    parser.add_argument('--ymax', type=int, required=True, help='Maximum y value of the ROI.')
    return parser.parse_args()

def filter_csv(input_csv, output_csv, xmin, xmax, ymin, ymax):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv, comment='#', names=['x', 'y', 'p', 't'])

    # Print the initial DataFrame for debugging
    print("Initial DataFrame:")
    print(df.head())

    # Filter the DataFrame based on the ROI for x and y
    filtered_df = df[(df['x'] >= xmin) & (df['x'] <= xmax) & (df['y'] >= ymin) & (df['y'] <= ymax)]

    # Print the filtered DataFrame for debugging
    print("Filtered DataFrame:")
    print(filtered_df.head())

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_csv, index=False, header=False)

def main():
    args = parse_args()
    output_dir = os.path.dirname(args.output_csv)
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filter_csv(args.input_csv, args.output_csv, args.xmin, args.xmax, args.ymin, args.ymax)
    print(f"Filtered CSV saved to {args.output_csv}")

if __name__ == "__main__":
    main()
