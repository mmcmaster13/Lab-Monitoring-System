import numpy as np
import statistics as stats

from make_useful import make_useful

#algorithm paper: https://github.com/JQIamo/Scanning-Transfer-Cavity-Lock/blob/master/Algorithm.pdf
#wider-scope paper: https://arxiv.org/pdf/1810.07256.pdf

def threshold_data(data, n_points):
    
    data_th = np.zeros(n_points)
    max_pt = np.max(data)
    
    for i in range(n_points-1):
        
        if data[i] < 0.5 * max_pt:
            data_th[i] = 0
        else:
            data_th[i] = data[i]
            
    return data_th

def get_derivative(points):
    
    derivative = (2*points[3] + points[2] - points[1] - 2*points[0])/10

    return derivative

def get_derivatives(data, n_points):
    
    #this will be used to find where the peaks are
    #inspired by https://github.com/JQIamo/Scanning-Transfer-Cavity-Lock/blob/master/STCL_Arduino_Code/STCL_Arduino_Code.ino
    
    derivatives = np.zeros(n_points-5)
    
    for i in range(2, n_points-3):
        
        indices = [i-2, i-1, i+1, i+2]
        points = data[indices]
        derivatives[i-2] = get_derivative(points)
        
    return derivatives

def find_peaks(derivatives, n_points):
    
    #we're going to loop over the derivatives and check for zero crossings AFTER significant negative derivatives
    
    n_points = n_points-5
    
    peak_locations = []
    
    flag = False
    
    for i in range(n_points):
        
        if derivatives[i] == 0 and not flag:
            continue
        elif derivatives[i] > 0 and not flag:
            flag = True
        elif derivatives[i] == 0 and flag:
            peak_locations.append(i)
            flag = False
        else:
            continue
    
    return peak_locations

def res_test(n_test, wait):
    
    peak_with_te = np.zeros(n_test)

    for i in range(n_test):
        data = rigol.query(":WAV:DATA?")
        
        useful_data = make_useful(data, n_points)
        data_th = threshold_data(useful_data, n_points)

        derivatives = get_derivatives(data_th, n_points)

        peak_locations_i = find_peaks(derivatives, n_points)
        
        peak_with_te[i] = peak_locations_i[0]*x_inc + x_origin

        time.sleep(wait)

    return peak_with_te

def get_var(rigol, n_iterations):

    var_positions = np.zeros(n_iterations)

    #ask the scope how many points it's sending
    n_points = int(rigol.query(":WAV:POIN?"))

    #ask for where the origin is on the trace
    x_origin = float(rigol.query(":WAV:XOR?"))
    
    #ask for time difference between sampled points
    x_inc = float(rigol.query(":WAV:XINC?"))
        
    for i in range(n_iterations):
    
        #ask for the trace data
        data = rigol.query(":WAV:DATA?")

        #turn the scope return into something actionable (split and cast to floats)
        useful_data = make_useful(data, n_points)

        #threshold the data, removing the noise away from the peaks
        data_th = threshold_data(useful_data, n_points)

        #take the derivatives of the curve at each set of ten points
        derivatives = get_derivatives(data_th, n_points)

        #find the peak locations using the derivatices
        peak_locations_i = find_peaks(derivatives, n_points)

        #calculate the variations in the peak position
        var_positions[i] = peak_locations_i[0]*x_inc + x_origin

        #calculate the variance in the differences of peak positions
        calculated_var =  stats.variance(var_positions)

    return calculated_var

def count_peaks(rigol):
    
    data = rigol.query(":WAV:DATA?")
    
    x_origin = float(rigol.query(":WAV:XOR?"))
    x_inc = float(rigol.query(":WAV:XINC?"))

    #print("X origin:", x_origin, "s")
    #print("X increments:", x_inc, "s")
    
    #ask the scope how many points it's sending
    n_points = int(rigol.query(":WAV:POIN?"))

    #x = np.arange(1400)
    x = np.arange(x_origin, x_origin + n_points * x_inc, x_inc)
        
    #keeping both thresholded and raw data just in case
    useful_data = make_useful(data, n_points)

    data_th = threshold_data(useful_data, n_points)
    
    derivatives = get_derivatives(data_th, n_points)
    x_d = np.arange(x_origin + 2*x_inc, x_origin + (n_points-3)*x_inc, x_inc)
    
    peak_locations = find_peaks(derivatives, n_points)
    
    return len(peak_locations)
    
