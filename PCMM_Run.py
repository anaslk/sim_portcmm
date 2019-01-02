import importlib as imp
import FeederModel as fm
import PID_controller as pid
import matplotlib.pyplot as plt

imp.reload(fm)
imp.reload(pid)


def feeders_sim(dt_s, pcmm, fd, m, fig, ax, n_fig, x_pause, Kp, Ki, Kd):

    # feeders initialisation
    sp_flowrate = fd.SP_feedflow(m.percent_composition, pcmm.Throughput)
    ffr = 0
    actual_weight = 0

    # Integral controller error initialisation
    error_i = 0

    # Derivative controller error initialisation
    error_d = 0

    # visualisation function

#    ax = fig.add_subplot(1, 1, 1)

    # visualisation parameters

    x_data_plot = []
    ffr_plot = []
    command_plot = []
    error_plot = []
    weight_plot = []
    sp_ffr_plot = []

    x_data_plot.append(0)
    ffr_plot.append(0)
    command_plot.append(0)
    error_plot.append(0)
    weight_plot.append(0)
    sp_ffr_plot.append(sp_flowrate)

    for i in dt_s:
        error, up = pid.proportional(sp_flowrate, ffr, Kp)
        error_i, ui = pid.integral(Ki, error, error_i, fd.max_screw_speed)
        error_d, ud = pid.derivate(Kd, error, error_d)
        command = pid.command(up, ui, ud)

        ffr, actual_weight = fd.feeder_flowrate(m.feedfactor_sigma, m.bulk_density, command, actual_weight)

        x_data_plot.append(i)
        ffr_plot.append(ffr)
        sp_ffr_plot.append(sp_flowrate)
        command_plot.append(command)
        error_plot.append(error)
        weight_plot.append(actual_weight)

        try:
            ax[n_fig].plot(x_data_plot, ffr_plot, 'b', linewidth=1)
            ax[n_fig].plot(x_data_plot, sp_ffr_plot, 'r', linewidth=2)
            ax[n_fig].grid(True)
            if x_pause != 0:
                plt.pause(x_pause)
        except TypeError:
            ax.plot(x_data_plot, ffr_plot, 'b', linewidth=1)
            ax.plot(x_data_plot, sp_ffr_plot, 'r', linewidth=2)
            ax.grid(True)
            if x_pause != 0:
                plt.pause(x_pause)
    return fig, weight_plot


def cmt_ops(cmt, weight):
    total = cmt.cmt_weight_update(weight)
    return total