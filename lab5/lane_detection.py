import cv2
import numpy as np
import math
from robomaster import robot
import time

def preprocess_image(image):
    """
    Process the image:
    - Crop out unwanted areas (remove the gripper).
    - Convert to HSV and apply a mask to extract the white lane.
    - Apply Canny edge detection.
    """
    height, width = image.shape[:2]
    roi = image[int(height * 0.5):, :]  # Crop lower half

    # Convert to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define HSV range for white color
    lower_white = np.array([0, 0, 200])  
    upper_white = np.array([255, 50, 255])

    # Create mask
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply Canny edge detection
    edges = cv2.Canny(mask, 50, 150)

    return edges, roi, mask

def get_lane_info(edges, roi):
    """
    Detect the lane and compute:
    - Center position
    - Angle of the lane (to adjust turning)
    """
    height, width = roi.shape[:2]

    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=100)

    if lines is not None:
        lane_midpoints = []
        angles = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            midpoint_x = (x1 + x2) // 2
            lane_midpoints.append(midpoint_x)

            # Compute lane angle (in degrees)
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)

            cv2.line(roi, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw lane lines

        if lane_midpoints:
            avg_lane_x = int(np.mean(lane_midpoints))  # Average X position of lane
            avg_angle = np.mean(angles) if angles else 0  # Average lane angle

            # Draw center point
            cv2.circle(roi, (avg_lane_x, height // 2), 5, (255, 0, 0), -1)

            return avg_lane_x, avg_angle

    return None, None  # No lane detected

def control_robot(ep_robot, lane_x, lane_angle, frame_width):
    """
    Move the robot to keep the lane centered & aligned with turns.
    """
    if lane_x is not None and lane_angle is not None:
        center_x = frame_width // 2  # Middle of the frame
        error = lane_x - center_x  # How far the lane is from center

        print(f"Lane angle: {lane_angle}")
        # Compute turn speed based on lane angle and position error
        turn_speed = np.clip(error * 0.05 + lane_angle * 0.01, -20, 20)

        print(f"Error: {error}")
        if abs(error) > 200:  
            ep_robot.chassis.drive_speed(x=0.15, y=0, z=turn_speed)  # Move forward + correct turn
        else:
            ep_robot.chassis.drive_speed(x=0.2, y=0, z=-lane_angle * 0.02)  # Move forward with slight turn
    else:
        ep_robot.chassis.drive_speed(x=0.1, y=0, z=0)  # Move forward if no lane detected

def main():
    """
    Main function to initialize the RoboMaster, capture video, process lane detection,
    and control movement.
    """
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_camera = ep_robot.camera
    ep_camera.start_video_stream(display=False)

    try:
        while True:
            frame = ep_camera.read_cv2_image(strategy="newest")
            edges, roi, mask = preprocess_image(frame)
            lane_x, lane_angle = get_lane_info(edges, roi)

            # Display processed images
            cv2.imshow("Edges", edges)
            cv2.imshow("Masked Lane", mask)
            cv2.imshow("Lane Detection", roi)

            control_robot(ep_robot, lane_x, lane_angle, frame.shape[1])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        ep_camera.stop_video_stream()
        ep_robot.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

