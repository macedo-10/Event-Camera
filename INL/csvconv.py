import os
import shutil
import time
import argparse
from tqdm import tqdm
from metavision_core.event_io import EventsIterator

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Monitor directory for new RAW files and convert to CSV.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    return parser.parse_args()

def convert_raw_to_csv(event_file_path, output_file, start_ts=0, max_duration=1e6*60, delta_t=1000000):
    mv_iterator = EventsIterator(input_path=event_file_path, delta_t=delta_t, start_ts=start_ts, max_duration=max_duration)

    with open(output_file, 'w') as csv_file:
        for evs in tqdm(mv_iterator, total=max_duration // delta_t):
            for (x, y, p, t) in evs:
                csv_file.write("%d,%d,%d,%d\n" % (x, y, p, t))

    print(f"Conversion completed: {output_file}")

def monitor_directory(source_dir, dest_dir):
    processed_files = set()
    while True:
        try:
            raw_files = [f for f in os.listdir(source_dir) if f.endswith('.raw') and f not in processed_files]
            for raw_file in raw_files:
                source_path = os.path.join(source_dir, raw_file)
                dest_path = os.path.join(dest_dir, raw_file)
                dest_csv = dest_path.replace('.raw', '.csv')

                if not os.path.exists(dest_csv):
                    shutil.copy(source_path, dest_path)
                    print(f"Copied {source_path} to {dest_path}")

                    convert_raw_to_csv(dest_path, dest_csv)

                processed_files.add(raw_file)
            time.sleep(10)
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)

def main():
    print("converting...")
    args = parse_args()
    source_dir = r"C:\Users\Pedro\Documents\metavision\recordings"
    dest_dir = r"C:\Users\Pedro\Desktop\INL"
    monitor_directory(source_dir, dest_dir)

if __name__ == "__main__":
    main()
