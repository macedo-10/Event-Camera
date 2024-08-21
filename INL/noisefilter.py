import numpy as np
from metavision_core.event_io import RawReader, DatWriter
from metavision_sdk_core.noise_filter import ActivityNoiseFilterAlgorithm, TrailFilterAlgorithm, SpatioTemporalContrastAlgorithm

# Define paths
input_path = "recording_2024-07-23_10-57-38-70Hz-20Vpp.raw"
output_path = "filtered_events.dat"

# Initialize reader
reader = RawReader(input_path)

# Initialize writer
writer = DatWriter(output_path, reader.get_size())

# Initialize noise filtering algorithms
activity_filter = ActivityNoiseFilterAlgorithm(width=reader.width, height=reader.height)
trail_filter = TrailFilterAlgorithm()
spatio_temporal_contrast_filter = SpatioTemporalContrastAlgorithm()

# Process and filter events
for evs in reader:
    # Apply the chosen noise filtering algorithm
    filtered_events = activity_filter.process_events(evs)
    # You can switch to another algorithm by uncommenting one of the following lines:
    # filtered_events = trail_filter.process_events(evs)
    # filtered_events = spatio_temporal_contrast_filter.process_events(evs)
    
    # Write filtered events to output file
    writer.write(filtered_events)

# Close the writer
writer.close()

print(f'Filtered events saved to {output_path}')
