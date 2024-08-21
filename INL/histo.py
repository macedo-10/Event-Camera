# Import necessary libraries
import os
import numpy as np
from matplotlib import pyplot as plt
from metavision_core.event_io import EventDatReader
from metavision_ml.preprocessing import histo
from metavision_ml.preprocessing.viz import viz_histo

# Set up matplotlib for inline display in Jupyter Notebooks

plt.rcParams['figure.figsize'] = [8, 6]

# Load the event data
path = "recording_2024-07-23_10-57-38-70Hz-20Vpp_cd.dat"  # Ensure spinner.dat is in the same directory as this script or provide the correct path
record = EventDatReader(path)
height, width = record.get_size()
print('Record dimensions: ', height, width)

start_ts = 1 * 1e6
record.seek_time(start_ts)  # Seek in the file to 1s

delta_t = 50000  # Sampling duration
events = record.load_delta_t(delta_t)  # Load 50 milliseconds worth of events
events['t'] -= int(start_ts)  # Important! Almost all preprocessing uses relative time!

# Set the number of time bins
tbins = 4

# Create an empty volume tensor
volume = np.zeros((tbins, 2, height, width), dtype=np.float32)

# Compute the histogram
histo(events, volume, delta_t)

# Visualize the histogram for the 2nd time bin
im = viz_histo(volume[1])
plt.imshow(im)
plt.tight_layout()
plt.title('Histogram', fontsize=20)
plt.show()
