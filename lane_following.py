from lane_detection import detect_lines, draw_lines, get_slopes_intercepts, detect_lanes, draw_lanes, IMAGE_WIDTH, IMAGE_HEIGHT

import cv2
import numpy as np

def get_lane_center(lanes):
    center_intercept = 0
    center_slope = 0
    min_dist_center = IMAGE_WIDTH

    for lane in lanes:
        slopes, intercepts = get_slopes_intercepts(lane)

        curr_slope = np.tan((np.arctan(slopes[0]) + np.arctan(slopes[1])) / 2)
        curr_intercept = (intercepts[0] + intercepts[1]) / 2

        if abs(IMAGE_WIDTH / 2 - curr_intercept) < min_dist_center:
            center_slope = curr_slope
            center_intercept = curr_intercept
            min_dist_center = abs(IMAGE_WIDTH / 2 - curr_intercept)
    
    return (center_intercept, center_slope)

def recommend_direction(center, slope):
    """
    Params
    - Center line intercept
    - Center line slope, currently unused

    Ret
    - Direction to move to, left, right, forward
    """
    if center < IMAGE_WIDTH / 2 - 50:
        return "left"
    elif center > IMAGE_WIDTH / 2 + 50:
        return "right"
    else:
        return "forward"