# Preprocessing Functions

# Load Libraries

import os
import numpy as np
from matplotlib import pyplot as plt  # graphic library, for plots
plt.rcParams['figure.figsize'] = [8, 6]

from metavision_core.event_io import EventDatReader

# Load Event Data
# In this tutorial, we will use a spinner sample data.
# Here is the link to download this DAT file: spinner.dat

# Let’s load the raw events to the variable events.

path = "spinner.dat"  # Ensure spinner.dat is in the same directory as this script or provide the correct path
record = EventDatReader(path)
height, width = record.get_size()
print('record dimensions: ', height, width)
start_ts = 1 * 1e6
record.seek_time(start_ts)  # seek in the file to 1s

delta_t = 50000  # sampling duration
events = record.load_delta_t(delta_t)  # load 50 milliseconds worth of events
events['t'] -= int(start_ts)  # important! almost all preprocessing use relative time!
print(events)
