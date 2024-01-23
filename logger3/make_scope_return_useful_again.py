import numpy as np

def make_useful(osc_str, n_points):
    
    data_arr_str = osc_str.split(",")
    
    data_arr_double = np.zeros(n_points-1)
    
    for i in range(n_points-1):
        
        if data_arr_str[i+1] != "\n":
            data_arr_double[i] = float(data_arr_str[i+1])
        else:
            data_arr_double[i+1] = 0.0
        
    return data_arr_double
