from math import sqrt

def calc_time_to_fall_in_ms(d_in_cm):
    """
    Calculates the time a obj
    will fall returns ms

    args:
        d_in_cm : the distance given as float/int that the object will fall
    """
    d = float(d_in_cm) / 100
    return sqrt(2 * d / 9.80665) * 1000
