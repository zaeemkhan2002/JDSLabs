import cv2
import numpy as np
from robomaster import robot
import time

def detect_object(image, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Draw the largest contour on the original image
        result = np.zeros_like(image)  # Create a black background
        cv2.drawContours(result, [largest_contour], -1, (0, 255, 0), 2)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(result, "Largest Contour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return (x, y, w, h), mask, result
    return None, mask, image

def estimate_distance(width, known_width=0.1, focal_length=800):
    return (known_width * focal_length) / width

def compute_angle(x, frame_width, fov=120):
    center_x = frame_width / 2
    angle = ((x - center_x) / center_x) * (fov / 2)
    return angle

def move_robot(ep_robot, distance, angle):
    ep_robot.chassis.move(x=distance, y=0, z=0, xy_speed=0.2).wait_for_completed()

def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_camera = ep_robot.camera
    ep_gripper = ep_robot.gripper
    ep_chassis = ep_robot.chassis

    lower_hsv = np.array([90, 50, 50])  # Lower bound for red color
    upper_hsv = np.array([140, 255, 255])  # Upper bound for red color
    min_distance_threshold = 0.35

    ep_camera.start_video_stream(display=False)
    ep_arm = ep_robot.robotic_arm 
    time.sleep(1)
    
    while True:
        img = ep_camera.read_cv2_image(strategy="newest")
        (x, y, w, h), mask, result = detect_object(img, lower_hsv, upper_hsv)

        # Display the mask and the detected contours
        cv2.imshow("Masked Object", mask)
        cv2.imshow("Largest Contour Detection", result)
        
        if x is not None:
            distance = estimate_distance(w)
       
            angle = compute_angle(x, img.shape[1])
            
            print(f"Distance: {distance}")
            if distance > min_distance_threshold:
                move_robot(ep_robot, min(distance * 0.25, 0.2), angle)
            else:
                break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(0.5)
        
    
    ep_chassis.move(x=0.075, y=0, z=0, xy_speed=0.2).wait_for_completed()
    time.sleep(2)
    ep_gripper.close()
    time.sleep(2)

    

    ep_arm.move(x=0, y=50).wait_for_completed()
    ep_chassis.move(x=-0.5, y=0, z=0, xy_speed=0.2).wait_for_completed()
    ep_gripper.open()
    ep_arm.move(x=0, y=-50).wait_for_completed()

    ep_camera.stop_video_stream()
    ep_robot.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
