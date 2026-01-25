import numpy as np
from scipy.optimize import least_squares

class Trilateration:
    def __init__(self, env):
        
        self.beacons = env.get_beacons()
        self.p0 = env.p0  # 환경의 P0 값 참조
        self.n = env.n    # 환경의 Path Loss 값 참조

    def rssi_to_distance(self, rssi):
        return 10 ** ((self.p0 - rssi) / (10 * self.n))

    def residuals(self, guess_pos, distances):
        est_distances = np.linalg.norm(self.beacons - guess_pos, axis=1)
        return est_distances - distances

    def estimate_position(self, rssi_values):
        measured_distances = self.rssi_to_distance(rssi_values)
        initial_guess = np.mean(self.beacons, axis=0)

        result = least_squares(
            self.residuals, 
            initial_guess, 
            args=(measured_distances,)
        )
        return result.x