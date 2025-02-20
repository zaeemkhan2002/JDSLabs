import math
import time
from robomaster import robot

class PIDController:
    def __init__(self, kp, ki, kd, dt, output_limit=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.output_limit = output_limit
        
        self.integral_error = 0.0
        self.previous_error = 0.0

    def reset(self):
        self.integral_error = 0.0
        self.previous_error = 0.0

    def compute_output(self, current_error):
        p_term = self.kp * current_error
        
        self.integral_error += current_error * self.dt
        i_term = self.ki * self.integral_error
        
        d_term = self.kd * (current_error - self.previous_error) / self.dt
        
        self.previous_error = current_error
        
        output = p_term + i_term + d_term

        if self.output_limit is not None:
            min_out, max_out = self.output_limit
            output = max(min_out, min(output, max_out))

        return output

def euclidean_distance(robot_x, robot_y, goal_x, goal_y):
    return math.sqrt((goal_x - robot_x)**2 + (goal_y - robot_y)**2)

def angle_difference(current_angle, target_angle):
    diff = (target_angle - current_angle) % (2.0 * math.pi)
    if diff > math.pi:
        diff -= 2.0 * math.pi
    return diff

def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis

    # Robot initial pose (x, y, theta)
    robot_x = 0.0
    robot_y = 0.0
    robot_theta = 0.0

    goal_x = 5.0
    goal_y = 0.0

    dt = 0.5
    dist_pid = PIDController(1.2, 0.0, 0.2, dt, output_limit=(-1.0, 1.0))
    ang_pid = PIDController(2.0, 0.0, 0.1, dt, output_limit=(-2.0, 2.0))

    distance_tolerance = 0.05
    angle_tolerance = 0.01

    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        dist_error = euclidean_distance(robot_x, robot_y, goal_x, goal_y)
        desired_theta = math.atan2(goal_y - robot_y, goal_x - robot_x)
        ang_error = angle_difference(robot_theta, desired_theta)

        if dist_error < distance_tolerance and abs(ang_error) < angle_tolerance:
            print("Goal reached!")
            break

        linear_cmd = dist_pid.compute_output(dist_error)
        angular_cmd = ang_pid.compute_output(ang_error)

        linear_cmd = max(-1.0, min(linear_cmd, 1.0))
        angular_cmd = max(-2.0, min(angular_cmd, 2.0))

        ep_chassis.move(x=linear_cmd * dt, y=0, z=angular_cmd * dt * 180 / math.pi, xy_speed=1.0).wait_for_completed()

        robot_x += linear_cmd * math.cos(robot_theta) * dt
        robot_y += linear_cmd * math.sin(robot_theta) * dt
        robot_theta += angular_cmd * dt
        robot_theta = (robot_theta + math.pi) % (2.0 * math.pi) - math.pi

        print(f"Time={elapsed_time:.2f}s | dist_error={dist_error:.2f} | ang_error={ang_error:.2f} "
              f"| linear_cmd={linear_cmd:.2f} | angular_cmd={angular_cmd:.2f} "
              f"| pose=({robot_x:.2f}, {robot_y:.2f}, {robot_theta:.2f})")

        time.sleep(dt)

    ep_robot.close()
    print("Controller stopped.")

if __name__ == "__main__":
    main()