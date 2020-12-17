from utils.track import get_points
import numpy as np

# Finds the direction corresponding to the position in which the object appears
# in the camera's frame. Assumes a linear relation between positions and angles.

def get_angles(camera, video):

    tracker = 7
    points = get_points(video, tracker)

    s = np.array([1920, 1080])  # Size of the frame
    v = camera.view

    angles = np.array([[0, 0]])

    for p in points:
        x = np.array([p[0], s[1] - p[1]])   # p = (0, 0) is the top left corner!?
        a = x/s*v - v/2

        # The vertical angle theta should be the first row of 'angles'
        angles = np.append(angles, [[a[1], a[0]]], axis=0)

    angles = angles[1:len(angles)]
    angles = angles + camera.dir

    return angles
