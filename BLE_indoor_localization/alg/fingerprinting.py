import numpy as np
from sklearn.neighbors import KNeighborsRegressor

class Fingerprint:
    def __init__(self, env, fg_config):
        self.env = env
        self.grid_size = fg_config["grid_size"]
        self.k = fg_config["k"]
        self.num_samples = fg_config["num_samples"]
        
        self.model = KNeighborsRegressor(n_neighbors=self.k, weights='distance')
        self.is_trained = False
        self.radio_map_rssi = []
        self.radio_map_pos = []

    def train_radio_map(self):
        width, height = self.env.width, self.env.height
        
        x_points = np.arange(0, width + 0.1, self.grid_size)
        y_points = np.arange(0, height + 0.1, self.grid_size)

        rssi_list = []
        pos_list = []

        total_points = len(x_points) * len(y_points)
        print(f"Building fingerprinting map (No. of points: {total_points}, sampling: {self.num_samples} times)")

        for x in x_points:
            for y in y_points:
                pos = [x, y]
                samples = []
                for _ in range(self.num_samples):
                    sample = self.env.get_rssi(pos, noise=True)
                    samples.append(sample)
                
                avg_rssi = np.mean(samples, axis=0)
                rssi_list.append(avg_rssi)
                pos_list.append(pos)

        self.radio_map_rssi = np.array(rssi_list)
        self.radio_map_pos = np.array(pos_list)

        self.model.fit(self.radio_map_rssi, self.radio_map_pos)
        self.is_trained = True
        print(f"Completed")

    def estimate_position(self, current_rssi):
        if not self.is_trained:
            raise Exception("Radio Map does not exist")
        
        current_rssi = np.array(current_rssi).reshape(1, -1)
        estimated_pos = self.model.predict(current_rssi)
        
        return estimated_pos[0]