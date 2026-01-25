import numpy as np

class IndoorNavigationEnv:
    def __init__(self, config, beacons_pos):
        
        #When defining parameters, use ENV_CONFIG from config.py
        #For beacons, use BEACONS
        self.width = config["width"]
        self.height = config["height"]
        self.p0 = config["p0"]
        self.n = config["n"]
        self.sigma = config["sigma"]   
        self.beacons = []

        for b in beacons_pos:
            self.add_beacon(b[0], b[1])


    def add_beacon(self, x, y):
        self.beacons.append([x, y])

    def get_beacons(self):
        return np.array(self.beacons)

    def get_rssi(self, true_pos, noise=True):
        #Using Path loss model

        beacons = np.array(self.beacons)
        true_pos = np.array(true_pos)
        
        #Calculate Euclidean distances from beacons to true location
        distances = np.linalg.norm(beacons - true_pos, axis=1)
        
        # Preventing log error (set dist to 0.1 when dist=0)
        distances = np.maximum(distances, 0.1)

        # RSSI = P0 - 10 * n * log10(d)
        rssi = self.p0 - 10 * self.n * np.log10(distances)

        # 3. Add Gaussian noise
        if noise:
            noise_val = np.random.normal(0, self.sigma, size=len(rssi))
            rssi += noise_val
            
        return rssi