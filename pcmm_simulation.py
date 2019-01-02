import importlib as imp
import FeederModel as fm
import PCMM_Run as prun
import Material_Init as mi

import matplotlib.pyplot as plt

imp.reload(fm)
imp.reload(prun)

# duration of simulation
dt_s = range(1, 300)

'''----------------------------------------------------
-------------------------------------------------------
PCMM creation and parametrisation
-------------------------------------------------------
----------------------------------------------------'''

pcmm1 = fm.PCMM(10, 5)

# API Glasdegib maleate
fd1 = fm.Feeders(60., 300., mi.API_topup_v, 6, mi.API_min_refill_v)
m1 = fm.Material(0.1, mi.API_bulk_density, 21.844)

# MCC Microcrystalline Cellulose
fd2 = fm.Feeders(60, 300, mi.MCC_topup_v, 6, mi.MCC_min_refill_v)
m2 = fm.Material(0.05, mi.MCC_bulk_density, 49.104)

# DCP Dibasic Calcium Phosphate, anhydrous
fd3 = fm.Feeders(60, 300, mi.DCP_topup_v, 6, mi.DCP_min_refill_v)
m3 = fm.Material(0.01, mi.DCP_bulk_density, 24.552)

# SSG Sodium Starch Glycolate
fd4 = fm.Feeders(60, 300, mi.SSG_topup_v, 6, mi.SSG_min_refill_v)
m4 = fm.Material(0.05, mi.SSG_bulk_density, 3)

# MgSt Magnesium Stearate
fd5 = fm.Feeders(60, 300, mi.MgSt_topup_v, 6, mi.MgSt_min_refill_v)
m5 = fm.Material(0.01, mi.MgSt_bulk_density, 1.5)

cmt1 = fm.CMT(60, 60, 500, 500, 150, 475, pcmm1.nb_active_feeders)

'''----------------------------------------------------
-------------------------------------------------------
PID parametrisation
-------------------------------------------------------
----------------------------------------------------'''

# Proportional controller parametrisation
Kp = 0.35

# Integral controller parametrisation
Ki = 0.5

# Derivative controller parametrisation
Kd = 0.02

'''----------------------------------------------------
-------------------------------------------------------
PCMM run and result visualisation
-------------------------------------------------------
----------------------------------------------------'''

# visualisation settings and initialisation
fig0, ax0 = plt.subplots(1, 1)
fig1, ax1 = plt.subplots(2, 1)
fig2, ax2 = plt.subplots(2, 1)
x_pause = 0

# RUN
g1, f1wgt = prun.feeders_sim(dt_s, pcmm1, fd1, m1, fig0, ax0, 0, x_pause, Kp, Ki, Kd)
g2, f2wgt = prun.feeders_sim(dt_s, pcmm1, fd2, m2, fig1, ax1, 0, x_pause, Kp, Ki, Kd)
g3, f3wgt = prun.feeders_sim(dt_s, pcmm1, fd3, m3, fig1, ax1, 1, x_pause, Kp, Ki, Kd)
g4, f4wgt = prun.feeders_sim(dt_s, pcmm1, fd2, m2, fig2, ax2, 0, x_pause, Kp, Ki, Kd)
g5, f5wgt = prun.feeders_sim(dt_s, pcmm1, fd3, m3, fig2, ax2, 1, x_pause, Kp, Ki, Kd)


#prun.cmt_ops(cmt1, f1wgt)

plt.show()