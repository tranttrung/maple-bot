import cv2
import numpy as np
import mss
import time

class Vision:
    def __init__(self):
        self.sct = mss.mss()
        # Define screen region to capture, None means full screen
        self.monitor = self.sct.monitors[1] 

    def capture_screen(self):
        # Grab the data
        sct_img = self.sct.grab(self.monitor)
        # Convert to numpy array
        img = np.array(sct_img)
        # Convert BGRA to BGR
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def extract_minimap(self, screen_img, rect=(0, 0, 300, 200)):
        """
        Extract minimap from the top left corner.
        rect is (x, y, width, height)
        """
        x, y, w, h = rect
        # Ensure we don't go out of bounds
        max_y, max_x = screen_img.shape[:2]
        return screen_img[y:min(y+h, max_y), x:min(x+w, max_x)]

    def find_player_on_minimap(self, minimap_img):
        """
        Find the yellow dot representing the player on the minimap.
        Returns (x, y) coordinates relative to the minimap, or None if not found.
        """
        hsv = cv2.cvtColor(minimap_img, cv2.COLOR_BGR2HSV)
        
        # Define color range for yellow dot. Adjust these values based on actual game colors
        # MapleStory yellow dot is usually bright yellow
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Assume the largest yellow blob is the player
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 1: # Filter out noise
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    return (cX, cY)
        return None

    def find_monster_on_screen(self, screen_img, template_img_path, threshold=0.7):
        """
        Find a monster on the screen using template matching.
        This is a basic approach. More advanced would be YOLO/cascade.
        """
        # Load template
        template = cv2.imread(template_img_path, cv2.IMREAD_COLOR)
        if template is None:
            return None
        
        # Perform template matching
        res = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            # Return center of the matched region
            h, w = template.shape[:2]
            return (max_loc[0] + w//2, max_loc[1] + h//2)
        return None

    # TODO: Add functions to read HP/MP bars
    # This requires cropping the specific HP/MP bar region and calculating the percentage of red/blue pixels
