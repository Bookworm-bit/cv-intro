import cv2
import numpy as np
import random

def detect_lines(img, threshold1=50, threshold2=150, aperture_size=3, minLineLength=100, maxLineGap=10):
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale_img, threshold1, threshold2)
    lines = cv2.HoughLinesP(
        edges,
        aperture_size,
        np.pi/180,
        minLineLength=minLineLength,
        maxLineGap=maxLineGap
    )

    return lines

def draw_lines(img, lines, color=(0, 255, 0)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
    
    return img

def get_slopes_intercepts(lines):
    slopes = []
    intercepts = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        slopes.append((y2 - y1) / (x2 - x1))

        # slope * (x - x1) + y1 = 0
        # x = -y1 / slope + x1
        intercepts.append(-y1 / slopes[-1] + x1)

    return (slopes, intercepts)

def detect_lanes(lines):
    lanes = []

    slopes, intercepts = get_slopes_intercepts(lines)

    for i in range(len(lines) - 1):
        if slopes[i] == slopes[i+1]:
            lanes.append([lines[i], lines[i+1]])

    return lanes

def draw_lanes(img, lanes):
    for lane in lanes:
        color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

        x1, y1, x2, y2 = lanes[0][0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)

        x1, y1, x2, y2 = lanes[1][0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
    
    return img