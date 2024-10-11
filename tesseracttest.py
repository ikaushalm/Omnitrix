import cv2
import numpy as np
from PIL import Image
from math import sqrt

# Load the image and convert it to grayscale
image_path = "DragonData.png"
image = Image.open(image_path)
image_rgb = image.convert("RGB")
image_np = np.array(image_rgb)
gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

# Use HoughCircles to detect circles in the image
circles = cv2.HoughCircles(
    gray_image,
    cv2.HOUGH_GRADIENT,
    dp=1.2,  # Inverse ratio of the accumulator resolution to the image resolution
    minDist=20,  # Minimum distance between detected centers
    param1=50,  # Higher threshold for Canny edge detector
    param2=30,  # Accumulator threshold for circle detection
    minRadius=10,  # Minimum circle radius
    maxRadius=30  # Maximum circle radius
)

# If circles are detected, process them
circle_colors_detected = []
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")

    # Sort circles by their x positions to identify columns
    circles = sorted(circles, key=lambda c: c[0])
    
    # Get the x-coordinate of the last column
    last_column_x = circles[-1][0]
    
    # Filter circles that are in the last column (based on x-coordinate proximity)
    last_column_circles = [c for c in circles if abs(c[0] - last_column_x) < 10]

    # Sort the last column circles by their y-coordinate to get them vertically
    last_column_circles = sorted(last_column_circles, key=lambda c: c[1])

    # Define the expected circle colors for mapping.
    circle_colors = {
        'D': (255, 0, 0),   # Red for 'D'
        'I': (0, 0, 255),   # Blue for '1'
        'T': (0, 255, 0)    # Green for 'T'
    }

    # Function to calculate the Euclidean distance between two RGB colors
    def color_distance(c1, c2):
        return sqrt(sum((c1[i] - c2[i]) ** 2 for i in range(3)))

    # Function to identify the closest color from the defined circle colors.
    def get_closest_circle_color(color):
        closest_color = min(circle_colors, key=lambda k: color_distance(color, circle_colors[k]))
        return closest_color

    # Analyze the last column circles and extract their colors
    for c in last_column_circles:
        x, y, r = c  # Circle center coordinates (x, y) and radius (r)
        # Define the bounding box for the circle area
        x_start = max(0, x - r)
        x_end = min(image_rgb.width, x + r)
        y_start = max(0, y - r)
        y_end = min(image_rgb.height, y + r)
        
        # Crop the region around the circle
        region = image_rgb.crop((x_start, y_start, x_end, y_end))
        colors = region.getcolors(maxcolors=1000)
        
        # Get the most common color in the region (assumes circle occupies most of the area)
        most_common_color = max(colors, key=lambda item: item[0])[1] if colors else (0, 0, 0)
        detected_color = get_closest_circle_color(most_common_color)
        
        # Append the detected color as a character ('D', '1', or 'T')
        circle_colors_detected.append(detected_color)

# Return the last two detected circle values
last_2_circle_values = circle_colors_detected[-2:]

print(circle_colors_detected)

print(last_2_circle_values)
