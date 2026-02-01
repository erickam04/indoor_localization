import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from sim.env import IndoorNavigationEnv
from alg.trilateration import Trilateration
from alg.fingerprinting import Fingerprint

def run_trajectory_test():
    #Initialization
    env = IndoorNavigationEnv(cfg.ENV_CONFIG, cfg.BEACONS, cfg.WALLS)
    tri_solver = Trilateration(env)
    fg_solver = Fingerprint(env, cfg.FG_CONFIG)
    fg_solver.train_radio_map()

    # Set time and trajectory
    dt = cfg.TRAJECTORY_CONFIG["dt"]
    total_time = cfg.TRAJECTORY_CONFIG["total_time"]
    steps = int(total_time / dt)
    start_pos = np.array(cfg.TRAJECTORY_CONFIG["start_pos"])
    velocity = np.array(cfg.TRAJECTORY_CONFIG["velocity"])


    true_path, tri_path, fg_path = [], [], []

    print(f"Trajectory simulation ({steps} steps)")

    for i in range(steps):
        # Calculate current pos
        current_true_pos = start_pos + velocity * (i * dt)
        
        # Retreive rssi
        rssi = env.get_rssi(current_true_pos)

        pos_tri = tri_solver.estimate_position(rssi)
        pos_fg = fg_solver.estimate_position(rssi)

        # Record
        true_path.append(current_true_pos.copy())
        tri_path.append(pos_tri)
        fg_path.append(pos_fg)

    # Convert list into numpy array
    true_path, tri_path, fg_path = map(np.array, [true_path, tri_path, fg_path])


    plt.figure(figsize=(10, 8))
    
    # Plot wall
    for w in env.walls:
        plt.plot([w.p1[0], w.p2[0]], [w.p1[1], w.p2[1]], 'k-', linewidth=3, label='Wall' if w == env.walls[0] else "")

    # Plot path
    plt.plot(true_path[:, 0], true_path[:, 1], 'g-', linewidth=2, label='True Path')
    plt.plot(tri_path[:, 0], tri_path[:, 1], 'b--', alpha=0.6, label='Trilateration')
    plt.plot(fg_path[:, 0], fg_path[:, 1], 'r--', alpha=0.6, label='Fingerprinting')

    # Plot beacons
    beacons = env.get_beacons()
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='^', s=100, label='Beacon')

    plt.xlabel("X (m)"); plt.ylabel("Y (m)")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.xlim(-1, 11); plt.ylim(-1, 11)
    plt.show()


run_trajectory_test()