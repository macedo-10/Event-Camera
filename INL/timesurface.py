# Import necessary libraries
import numpy as np
from matplotlib import pyplot as plt
from metavision_core.event_io import EventDatReader
from metavision_ml.preprocessing import timesurface
from metavision_ml.preprocessing.viz import filter_outliers

# Function to visualize linear time surface
def visualize_linear_time_surface(events, height, width, delta_t, tbins):
    volume = np.zeros((tbins, 2, height, width))
    timesurface(events, volume, delta_t, normed=True)
    
    plt.imshow(filter_outliers(volume[1, 0], 7))
    plt.tight_layout()
    plt.colorbar()
    plt.title('Linear Time Surface', fontsize=20)
    plt.show()

# Function to visualize exponential-decay time surface
def visualize_exponential_decay_time_surface(events, height, width, delta_t, larger_delta_t, tbins):
    volume = np.zeros((1, 2, height, width))
    timesurface(events, volume, larger_delta_t, normed=False)

    v1 = np.exp(-(delta_t - volume) / 5e4)
    v2 = np.exp(-(delta_t - volume) / 5e5)

    fig, axes_array = plt.subplots(nrows=2, ncols=2)
    
    im0 = axes_array[0, 0].imshow(v1[0, 0])
    fig.colorbar(im0, ax=axes_array[0, 0], shrink=1)
    
    im1 = axes_array[1, 0].imshow(v1[0, 1])
    fig.colorbar(im1, ax=axes_array[1, 0], shrink=1)
    
    im2 = axes_array[0, 1].imshow(v2[0, 0])
    fig.colorbar(im2, ax=axes_array[0, 1], shrink=1)
    
    im3 = axes_array[1, 1].imshow(v2[0, 1])
    fig.colorbar(im3, ax=axes_array[1, 1], shrink=1)
    
    axes_array[0, 0].set_ylabel("Polarity 0")
    axes_array[1, 0].set_ylabel("Polarity 1")
    axes_array[1, 0].set_xlabel("τ 0.05s")
    axes_array[1, 1].set_xlabel("τ 0.5s")
    
    plt.tight_layout()
    fig.subplots_adjust(top=0.88)
    fig.suptitle('Exponential-Decay Time Surface', fontsize=20)
    plt.show()

# Load the event data
path = "recording_2024-07-23_10-57-38-70Hz-20Vpp_cd.dat"  # Ensure spinner.dat is in the same directory as this script or provide the correct path
record = EventDatReader(path)
height, width = record.get_size()
print('Record dimensions: ', height, width)

# Linear Time Surface
start_ts = 1 * 1e6
record.seek_time(start_ts)  # Seek in the file to 1s
delta_t = 50000  # Sampling duration
events = record.load_delta_t(delta_t)  # Load 50 milliseconds worth of events
events['t'] -= int(start_ts)  # Important! Almost all preprocessing uses relative time!

tbins = 4
visualize_linear_time_surface(events, height, width, delta_t, tbins)

# Exponential-Decay Time Surface
record.seek_time(3 * 1e6)  # Seek in the file to 3s
larger_delta_t = 1000000  # 1s
timesurface_events = record.load_delta_t(larger_delta_t)  # Load 1s of events
timesurface_events['t'] -= int(3 * 1e6)

visualize_exponential_decay_time_surface(timesurface_events, height, width, delta_t, larger_delta_t, tbins)
