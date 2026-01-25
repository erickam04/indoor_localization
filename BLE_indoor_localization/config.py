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

# Object/Wall Placement - TODO

# Fingerprinting
FG_CONFIG = {
    "grid_size": 1.0,   # 격자 간격 (m)
    "k": 3,             # KNN k값
    "num_samples": 10   # 학습 시 샘플링 횟수
}

# True position
TEST_POS = [3.5, 6.5]