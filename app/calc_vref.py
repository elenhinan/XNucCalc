#!/usr/bin/env python3
import numpy as np
from scipy.optimize import curve_fit

def calc_vref(voltage, amplitude):
    #convert to numpy arrays
    a = np.array(amplitude, dtype=np.float)
    v = np.array(voltage, dtype=np.float)
    
    # mask out values not greater than 0
    mask = a > 0

    # only do curve fitting if more than two valid points
    if(np.sum(mask) >= 2):
        v = v[mask]
        a = a[mask]

        # starting point for estimation
        p0 = [150,120]

        flip_angle = lambda x, v_ref, a_max: np.sin(x/v_ref*np.pi/2)*a_max
        v_ref, a_max = curve_fit(flip_angle, v, a, p0, np.sqrt(a))[0]
        fit_v = np.arange(0, 250, 5)
        fit_a = flip_angle(fit_v, v_ref, a_max)
        return v_ref, fit_v.tolist(), fit_a.tolist()

    # else return flat output curve and no v_ref value
    else:
        return 'NaN', [0,voltage[-1]], [0,0]