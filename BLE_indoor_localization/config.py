# Experiment Configurations

# Environment
ENV_CONFIG = {
    "width": 10,        
    "height": 10,       
    "p0": -55,          # Unit RSSI (1m)
    "n": 3.0,           # Path Loss Exponent
    "sigma": 2.0        # Noise standard deviation
}

# Beacon Placement
BEACONS = [
    [0, 0],
    [10, 0],
    [0, 10],
    [10, 10]
]

# Object/Wall Placement
WALLS = [
    [1.0, 9.0, 2.0, 9.0],
    [1.0, 8.0, 2.0, 8.0],
    [1.0, 9.0, 1.0, 8.0],
    [2.0, 9.0, 2.0, 8.0],

    [8.0, 1.0, 8.0, 2.0],
    [9.0, 1.0, 9.0, 2.0],
    [8.0, 1.0, 9.0, 1.0],
    [8.0, 2.0, 9.0, 2.0]
]


# Fingerprinting
FG_CONFIG = {
    "grid_size": 1.0,   # 격자 간격 (m)
    "k": 3,             # KNN k값
    "num_samples": 10   # 학습 시 샘플링 횟수
}

# Test position
TEST_POS = [3.5, 6.5]

# Trajectory and time
TRAJECTORY_CONFIG = {
    "dt": 0.2,
    "total_time": 10.0,
    "start_pos": [1.0, 1.0],
    "velocity": [0.8, 0.6]
}
