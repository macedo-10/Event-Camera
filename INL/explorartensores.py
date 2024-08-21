# Import necessary libraries
import os
import numpy as np
import h5py
from matplotlib import pyplot as plt
from metavision_ml.preprocessing.viz import filter_outliers

# Define the path to the HDF5 file
output_path = "recording_2024-07-23_10-57-38-70Hz-20Vpp.h5"

# Open the HDF5 tensor file in read mode
f = h5py.File(output_path, 'r')

# Print the 'data' dataset
print(f['data'])

# Get and print the shape and dtype attributes
hdf5_shape = f['data'].shape
print("Shape of the data: ", hdf5_shape)
print("Data type: ", f['data'].dtype)

# Print the attributes associated with the dataset
print("Attributes :\n")
for key in f['data'].attrs:
    print('\t', key, ' : ', f['data'].attrs[key])

# Visualize the data stored within the HDF5 tensor file
for i, timesurface in enumerate(f['data'][:10]):
    plt.imshow(filter_outliers(timesurface[0], 7))  # Filter out some noise
    plt.title("{:s} feature computed at time {:d} μs".format(f['data'].attrs['events_to_tensor'],
                                                             f['data'].attrs["delta_t"] * i))
    plt.pause(0.01)
    plt.show()

# Close the HDF5 file
f.close()
