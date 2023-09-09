import numpy as np

class ImgProcess:

    def __init__(self, cam=None, CV=None, motor=None) -> None:
        # Define default bounds for tracking yellow color in HSV format
        self.lower_bound, self.upper_bound = np.array([20, 100, 100]), np.array([30, 255, 255])
        
        # Reference to OpenCV module
        self.CV = CV
        
        # Reference to camera module
        self.cam = cam
        
        # Reference to motor control module
        self.motor = motor

    # Private method to select and capture the region of interest (ROI)
    def _capture_roi(self):
        # Capture a frame from the camera
        ret, frame = self.cam.read()

        # Display a window to select the ROI
        r = self.CV.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
        
        # Close all OpenCV windows
        self.CV.destroyAllWindows()

        # Extract the selected region from the frame
        roi = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

        # Convert the extracted region to HSV color space
        roi_hsv = self.CV.cvtColor(roi, self.CV.COLOR_BGR2HSV)

        # Calculate the average color of the selected region in HSV
        average_color = np.mean(roi_hsv, axis=(0, 1))

        # Define bounds for color tracking based on the average color of the ROI
        color_range = 20
        self.lower_bound = np.array([average_color[0] - color_range, 50, 50])
        self.upper_bound = np.array([average_color[0] + color_range, 255, 255])

        # Return the color bounds
        return self.lower_bound, self.upper_bound

    def capture_image(self):
        # Placeholder function to capture images (to be implemented)
        pass

    def start_process(self):
        # Infinite loop to keep processing the frames
        while True:
            # Capture a frame
            ret, frame = self.cam.read()
            
            # Display the live webcam feed
            self.CV.imshow('Webcam Feed', frame)
            
            # Detect key presses
            key = self.CV.waitKey(1) & 0xFF

            # Check if 's' key is pressed to select a new object for tracking
            if key == ord('s'):
                self.lower_bound, self.upper_bound = self._capture_roi()
                continue
            # Check if 'q' key is pressed to quit the application
            elif key == ord('q'):
                break

            # If color bounds are set, process the frame for object tracking
            if self.lower_bound is not None:
                # Convert the frame to HSV color space
                hsv = self.CV.cvtColor(frame, self.CV.COLOR_BGR2HSV)
                
                # Create a binary mask where the tracked color is in the range
                mask = self.CV.inRange(hsv, self.lower_bound, self.upper_bound)

                # Find contours in the mask
                contours, _ = self.CV.findContours(mask, self.CV.RETR_EXTERNAL, self.CV.CHAIN_APPROX_SIMPLE)

                # If any contours are found
                if contours:
                    # Get the largest contour (assumed to be the object being tracked)
                    c = max(contours, key=self.CV.contourArea)

                    # Calculate the center and radius of the object
                    (x, y), radius = self.CV.minEnclosingCircle(c)
                    center = (int(x), int(y))
                    radius = int(radius)

                    # Calculate the center of the frame
                    frame_center_x, frame_center_y = frame.shape[1] // 2, frame.shape[0] // 2

                    # Define movement sensitivity
                    threshold = 50

                    # Move the robot to keep the object in the center of the frame
                    if abs(center[0] - frame_center_x) > threshold:
                        if center[0] < frame_center_x:
                            self.motor.move_left()
                        else:
                            self.motor.move_right()
                    elif abs(center[1] - frame_center_y) > threshold:
                        if center[1] < frame_center_y:
                            self.motor.move_forward()
                        else:
                            self.motor.move_backward()
                    else:
                        self.motor.stop_motors()

                    # Draw a circle around the detected object on the frame
                    self.CV.circle(frame, center, radius, (0, 255, 0), 2)

                    # Display the tracking results
                    self.CV.imshow('Tracking Result', frame)

        # Release the camera and close all windows when done
        self.cam.release()
        self.CV.destroyAllWindows()
