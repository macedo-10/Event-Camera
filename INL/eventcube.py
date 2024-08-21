# Import necessary libraries
import numpy as np
from matplotlib import pyplot as plt
from metavision_core.event_io import EventDatReader
from metavision_ml.preprocessing import event_cube
from metavision_ml.preprocessing.viz import viz_event_cube_rgb, filter_outliers

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

# Create an empty volume tensor with 6 channels (3 micro time bins per polarity)
volume = np.zeros((1, 6, height, width), dtype=np.float32)

# Compute the Event Cube
event_cube(events, volume, delta_t)

# Visualize the Event Cube for each micro time bin and polarity
plt.figure()
fig, axes_array = plt.subplots(nrows=2, ncols=3)
for i in range(6):
    polarity = i % 2
    microtbin = i // 2
    img = volume[0, i]
    img = filter_outliers(img, 2)
    img = (img - img.min()) / (img.max() - img.min())
    axes_array[polarity, microtbin].imshow(img)

axes_array[0, 0].set_ylabel("Polarity 0")
axes_array[1, 0].set_ylabel("Polarity 1")
axes_array[1, 0].set_xlabel("1st µtbin")
axes_array[1, 1].set_xlabel("2nd µtbin")
axes_array[1, 2].set_xlabel("3rd µtbin")

plt.suptitle('Event Cube with 3 micro time bins \n per polarity', fontsize=20)
plt.tight_layout()
plt.show()

# Visualize the RGB representation of the micro time bins for events with positive polarity
img = viz_event_cube_rgb(volume[0])
plt.figure()
plt.imshow(img)
plt.title("RGB visualization of the micro time bins", fontsize=20)
plt.tight_layout()
plt.show()
