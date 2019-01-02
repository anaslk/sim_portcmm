import FeederModel as fm
import numpy as np


def proportional(sp_flowrate, actual_flowrate, Kp):
    error = sp_flowrate - actual_flowrate
    up = Kp*error
    return error, up


def integral(Ki, error, error_i, clamp_parameter):
    ui = Ki*(error + error_i)
    if ui > clamp_parameter:
        error_i = error_i
        ui = clamp_parameter
    else:
        error_i = error + error_i
    return error_i, ui


def derivate(Kd, error, error_d):
    ud = Kd*(error - error_d)
    error_d = error
    return error_d, ud


def command(up = 0, ui = 0, ud = 0):
    return up + ui + ud


def tuning(sp, ffr):
    return 100*ffr/sp