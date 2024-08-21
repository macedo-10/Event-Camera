# Import necessary libraries
import os
import numpy as np
import h5py
from matplotlib import pyplot as plt
from metavision_ml.preprocessing.viz import filter_outliers
from metavision_ml.preprocessing.hdf5 import generate_hdf5

# Define the input path for the raw file
input_path = "recording_shaker-1Hz-40mVpp-20mVsemlente.raw"

# Define the output folder and output path
output_folder = "."
output_path = output_folder + os.sep + os.path.basename(input_path).replace('.raw', '.h5')

# Check if the output file already exists, if not, generate it
if not os.path.exists(output_path):
    generate_hdf5(paths=input_path, output_folder=output_folder, preprocess="timesurface", delta_t=250000, height=None, width=None,
                  start_ts=0, max_duration=None)

# Print the sizes of the original and result files
print('\nOriginal file \"{}" is of size: {:.3f}MB'.format(input_path, os.path.getsize(input_path)/1e6))
print('\nResult file \"{}" is of size: {:.3f}MB'.format(output_path, os.path.getsize(output_path)/1e6))
