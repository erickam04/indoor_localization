import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from sim.env import IndoorNavigationEnv
from alg.fingerprinting import Fingerprint

def visualize_result(env, solver, true_pos, est_pos):
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Radio Map Grid
    if solver.is_trained:
        rp_x = solver.radio_map_pos[:, 0]
        rp_y = solver.radio_map_pos[:, 1]
        ax.scatter(rp_x, rp_y, c='gray', s=15, alpha=0.3, label='Map Grid')

    # Draw Beacons
    beacons = env.get_beacons()
    ax.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='^', s=150, label='Beacon', zorder=5)

    # True and Est positions
    ax.scatter(true_pos[0], true_pos[1], c='green', marker='*', s=250, label='True Position', zorder=6)
    ax.scatter(est_pos[0], est_pos[1], c='blue', marker='x', s=150, label='Est Position', zorder=6)
    
    # Error
    ax.plot([true_pos[0], est_pos[0]], [true_pos[1], est_pos[1]], 'k--', alpha=0.6)
    
    # Error dist.
    error_dist = np.linalg.norm(true_pos - est_pos)
    mid_x, mid_y = (true_pos + est_pos) / 2
    ax.text(mid_x + 0.2, mid_y, f"{error_dist:.2f}m", fontsize=9)

    #Map config
    ax.set_xlim(-1, env.width + 1)
    ax.set_ylim(-1, env.height + 1)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    ax.set_title(f"Fingerprinting Result")
    
    plt.show()

def run_test():
    print(f"Fingerprinting Test")

    #Print test config
    print("[Current Config]")
    print(f"Environment: {cfg.ENV_CONFIG}")
    print(f"beacons: {cfg.BEACONS}")
    print(f"Fingerprint : {cfg.FG_CONFIG}")


    # Initialize environment and Engine
    env = IndoorNavigationEnv(cfg.ENV_CONFIG, cfg.BEACONS)
    solver = Fingerprint(env, cfg.FG_CONFIG)

    # Offline Phase
    solver.train_radio_map()

    # Online Phase
    true_pos = np.array(cfg.TEST_POS)
    rssi_measurement = env.get_rssi(true_pos, noise=True)
    est_pos = solver.estimate_position(rssi_measurement)

    # Results
    error = np.linalg.norm(true_pos - est_pos)
    print(f"실제 위치: {true_pos}")
    print(f"추정 위치: {np.round(est_pos, 2)}")
    print(f"오차 거리: {error:.4f} m")

    visualize_result(env, solver, true_pos, est_pos)


run_test()