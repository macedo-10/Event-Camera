



from scipy import constants as konst
import numpy as np
# Implements a linear Kalman filter.
#import numpy


class KalmanFilterLinear:
  def __init__(self,_A, _B, _H, _x, _P, _Q, _R):
    self.A = _A                      # State transition matrix.
    self.B = _B                      # Control matrix.
    self.H = _H                      # Observation matrix.
    self.current_state_estimate = _x # Initial state estimate.
    self.current_prob_estimate = _P  # Initial covariance estimate.
    self.Q = _Q                      # Estimated error in process.
    self.R = _R                      # Estimated error in measurements.
  def GetCurrentState(self):
    return self.current_state_estimate
  def GetCurrentProbability(self):
    return self.current_prob_estimate
  def Step(self,control_vector,measurement_vector):
    #---------------------------Prediction step-----------------------------
    predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
    predicted_prob_estimate = (self.A * self.current_prob_estimate) * np.transpose(self.A) + self.Q
    #--------------------------Observation step-----------------------------
    innovation = measurement_vector - self.H*predicted_state_estimate
    innovation_covariance = self.H*predicted_prob_estimate*np.transpose(self.H) + self.R
    #-----------------------------Update step-------------------------------
    kalman_gain = predicted_prob_estimate * np.transpose(self.H) * np.linalg.inv(innovation_covariance)
    self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation
    # We need the size of the matrix so we can make an identity matrix.
    size = self.current_prob_estimate.shape[0]
    # eye(n) = nxn identity matrix.
    self.current_prob_estimate = (np.eye(size)-kalman_gain*self.H)*predicted_prob_estimate
    
  def Step_NoSave(self,control_vector,measurement_vector):
    """ Doesnt update latest prediction """
    #---------------------------Prediction step-----------------------------
    predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
    predicted_prob_estimate = (self.A * self.current_prob_estimate) * np.transpose(self.A) + self.Q
    #--------------------------Observation step-----------------------------
    innovation = measurement_vector - self.H*predicted_state_estimate
    innovation_covariance = self.H*predicted_prob_estimate*np.transpose(self.H) + self.R
    #-----------------------------Update step-------------------------------
    kalman_gain = predicted_prob_estimate * np.transpose(self.H) * np.linalg.inv(innovation_covariance)
    current_state_estimate = predicted_state_estimate + kalman_gain * innovation
    # We need the size of the matrix so we can make an identity matrix.
    size = self.current_prob_estimate.shape[0]
    # eye(n) = nxn identity matrix.
    current_prob_estimate = (np.eye(size)-kalman_gain*self.H)*predicted_prob_estimate
    return current_state_estimate, current_prob_estimate


class KalmanTracking(object):
    """ Class object to handle the tracking of a variable using Kalman filtering
    """
    
    def __init__(self,data=None):
        
        self._Kalman = None
        self.measurements = []
        self.predictions = []
        self.probabilities = []
        self.cov = 100
        self.error_proc = 0.0001 # Estimated error in process.
        self.error_measurement=1 # Estimated error in measurements.
        if data is not None:
            self.initKalmanState(data)

    # Property getters and setters
    @property
    def probability(self):
        return self.probabilities[-1]
    
    @property
    def prediction(self):
        return self.predictions[-1]
    
    @property
    def measurement(self):
        return self.measurements[-1]


    def __call__(self,data,noSave=False):
        if noSave:
            estimate = self.__stepKalmanNoSave(data)
            return estimate
        return self.__stepKalman(data)
    
    def __initKalmanState(self,state):
        """Creates a KalmanFilterLinear object with the initial estimate"""
        
        #cov = 0.00001
        #error_proc = 0.00001
        #error_measurement = 0.0001
        #print 'Initializing KalmanTracking with '
        Al = np.matrix([1])
        Hl = np.matrix([1])
        Bl = np.matrix([0])
        xhatl = np.matrix([state])
        Pl    = np.matrix([self.cov])
        Ql = np.matrix([self.error_proc])   # Estimated error in process.
        Rl = np.matrix([self.error_measurement])  # Estimated error in measurements.
                #Declare Filters
        self._Kalman = KalmanFilterLinear(Al,Bl,Hl,xhatl,Pl,Ql,Rl)
        self.measurements = []
        self.predictions = []
        self.probabilities = []
        return self._Kalman
    
    def __stepKalman(self,value):
        if self._Kalman is None:
            self.__initKalmanState(value)
        
        self.measurements.append(value)
        self._Kalman.Step(np.matrix([0]),np.matrix([value]))
        prediction = self._Kalman.GetCurrentState()[0,0]
        probability = self._Kalman.GetCurrentProbability()[0,0]
        self.predictions.append(prediction)
        self.probabilities.append(probability)
        return prediction

    def __stepKalmanNoSave(self,value):
        if self._Kalman is None:
            return value
        prediction, probability = self._Kalman.Step_NoSave(
                                                np.matrix([0]),
                                                np.matrix([value]))
        return prediction[0,0]
    

    