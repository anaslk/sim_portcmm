import numpy as np


# PCMM methods and properties

class PCMM:
    def __init__(self, Throughput, nb_active_feeders):
        self.Throughput = Throughput  # kg.h^-1
        self.nb_active_feeders = nb_active_feeders





# Feeders method and properties

class Feeders:
    def __init__(self, max_screw_speed, Recipient_Topup_Vol, Screw_Length,
                 Pitch_Length, Min_Refill):
        self.max_screw_speed = max_screw_speed  # rad.s^-1
        self.Recipient_Topup_Vol = Recipient_Topup_Vol/1000  # dm³ -> mL
        self.Screw_Length = Screw_Length  # mm
        self.Pitch_Length = Pitch_Length  # mm
        self.Min_Refill = Min_Refill  # mL

# ---------------------------------------------------------------------------------------
# Feeder Conversion Methods
# ---------------------------------------------------------------------------------------

    def conv_vol_mass(self, bulk_density):
        return self.Min_Refill * bulk_density, self.Recipient_Topup_Vol * bulk_density

    def pitchquantity(self):
        return round(self.Screw_Length / self.Pitch_Length)

    def SP_feedflow(self, percent_comp, th_put):
        return percent_comp * (th_put * 3.6)  # kg.h^-1 -> g.s^-1

    def feedfactor(self, feedfactor_sigma, actual_weight):
        FF = 0.643 * (1 - np.expm1(-actual_weight / 65))  # g.rev^-1
        return abs(np.random.normal(FF, feedfactor_sigma))

# --------------------------------------------------------------------------------------
# Feeder Operational Methods
# --------------------------------------------------------------------------------------

    def weight_update(self, actual_weight, bulk_density, flowrate=0):

        min_refill, topup_mass = self.conv_vol_mass(bulk_density)

        if actual_weight == 0:
            actual_weight = topup_mass

        else:
            actual_weight = actual_weight - flowrate

            if actual_weight < 0:
                actual_weight = 0
            elif actual_weight <= min_refill:
                actual_weight = topup_mass - min_refill + actual_weight

        return actual_weight

    def feeder_flowrate(self, feedfactor_sigma, bulk_density, screw_speed=0, actual_weight=0):

        if screw_speed > self.max_screw_speed:
            screw_speed = self.max_screw_speed
        elif screw_speed < -1 * self.max_screw_speed:
            screw_speed = -1 * self.max_screw_speed

        flowrate = self.feedfactor(feedfactor_sigma, actual_weight) \
                   * screw_speed
        actual_weight = self.weight_update(actual_weight, bulk_density, flowrate)

        return flowrate, actual_weight





# Composition material properties

class Material:
    def __init__(self, feedfactor_sigma, bulk_density, percent_composition):
        self.feedfactor_sigma = feedfactor_sigma
        self.bulk_density = np.random.normal(bulk_density, 0.05)  # # g.mL^-1
        self.percent_composition = percent_composition / 100  # in % of total composition





class CMT:
    def __init__(self, max_impeler1_sd, max_impeler2_sd, cmt_max_weight,
                 cmt_height, cmt_width, hum, nbf):
        self.max_impeler1_sd = max_impeler1_sd
        self.max_impeler2_sd = max_impeler2_sd
        self.cmt_max_weight = cmt_max_weight
        self.cmt_height = cmt_height
        self.cmt_width = cmt_width
        self.hum = hum
        self.total_weight = np.zeros(nbf)

    def cmt_weight_update(self, feeder_weight):
        for i in range(0, len(self.total_weight)):
            self.total_weight[i] = feeder_weight
        cmt_weight = sum(self.total_weight)
        return cmt_weight
