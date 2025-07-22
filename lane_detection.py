import cv2
import numpy as np
import random

IMAGE_HEIGHT = 2138
IMAGE_WIDTH = 3824

def detect_lines(img, threshold1=50, threshold2=150, aperture_size=3, minLineLength=100, maxLineGap=10):
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale_img, threshold1, threshold2, apertureSize=aperture_size)

    lines = cv2.HoughLinesP(
        edges,
        rho=aperture_size,
        theta=np.pi/180,
        threshold=100,
        minLineLength=minLineLength,
        maxLineGap=maxLineGap
    )

    return lines

def draw_lines(img, lines, color=(0, 255, 0)):
    if lines is None:
        return img

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
    
    return img

def get_slopes_intercepts(lines):
    """
    Returns slopes and horizontal intercepts with the bottom of an image for a set of images

    Params
    - lines: list of lines

    Ret
    - (slopes, intercepts): tuple of slopes then intercepts
    """
    slopes = []
    intercepts = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        slopes.append((y2 - y1) / (x2 - x1))

        intercepts.append((IMAGE_HEIGHT - y1) / slopes[-1] + x1)

    return (slopes, intercepts)

def detect_lanes(lines):
    lanes = []

    slopes, intercepts = get_slopes_intercepts(lines)
    
    filtered_lines = set()
    seen = [False] * len(lines)
    for i in range(len(lines)):
        if seen[i]:
            continue
        
        for j in range(i+1, len(lines)):
            if seen[j]:
                continue

            int_sim = abs(intercepts[i] - intercepts[j]) <= 50
            ang_sim = abs((np.arctan(slopes[i]) - np.arctan(slopes[j]) + 2 * np.pi) % (2 * np.pi) - 2 * np.pi) <= 0.1

            if int_sim or ang_sim:
                seen[j] = True
        
        filtered_lines.add(i)

    filtered_lines = list(filtered_lines)
    
    for i in range(len(filtered_lines)):
        for j in range(i+1, len(filtered_lines)):
            angle1 = np.arctan(filtered_lines[i])
            angle2 = np.arctan(filtered_lines[j])

            ang_sim = abs((angle1 - angle2 + 360) % 360) <= 0.5
            int_sim = abs(intercepts[filtered_lines[i]] - intercepts[filtered_lines[j]]) <= 500

            if ang_sim or int_sim:
                lanes.append([lines[filtered_lines[i]], lines[filtered_lines[j]]])

    return lanes

def draw_lanes(img, lanes):
    for lane in lanes:
        color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

        x1, y1, x2, y2 = lane[0][0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)

        x1, y1, x2, y2 = lane[1][0]
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
    
    return img