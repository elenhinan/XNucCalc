#!/usr/bin/env python3
import numpy as np
from scipy.optimize import curve_fit

def calc_vref(voltage, amplitude):
    #v = np.array([10, 40, 70, 100, 130, 160, 190, 220])
    #a = np.array([334, 1297, 2168, 2819, 3222, 3379, 3215, 2768])
    v = np.array(voltage)
    a = np.array(amplitude)

    p0 = [150,3000]

    flip_angle = lambda x, v_ref, a_max: np.sin(x/v_ref*np.pi/2)*a_max
    v_ref, a_max = curve_fit(flip_angle, v, a, p0)[0]
    
    fit_v = np.arange(0, 250, 5)
    fit_a = flip_angle(fit_v, v_ref, a_max)

    return v_ref, fit_v.tolist(), fit_a.tolist()