%matplotlib inline

import numpy as np

from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [11, 7]

from metavision_sdk_core import BaseFrameGenerationAlgorithm
import metavision_sdk_ml

def are_events_equal(ev1, ev2):
    """Simple functions comparing event vector field by fields"""
    return ev1.size == ev2.size and min(np.allclose(ev1[name], ev2[name]) for name in ev1.dtype.names)

import os
from metavision_core.event_io import RawReader

sequence_filename_raw = "recording_2024-07-23_11-02-22-80Hz-20Vpp.raw"