import numpy as np
from utils.angles import get_angles

def direction(angles):

    # Returns a unit vector pointing in the direction angles = (theta, phi)
    # (theta, phi) = (0, 0) points straight ahead

    theta = angles[0]
    phi = angles[1]

    n = np.array([np.cos(theta)*np.sin(phi),
                  np.cos(theta)*np.cos(phi),
                  np.sin(theta)])

    return n

def intersection(r1, r2, n1, n2):

    # Finds the intersection of the lines passing through the points r1, r2 and
    # going in the directions n1, n2. The lines usually do not intersect, so
    # the 'intersection' is taken as the midpoint of the shortest line segment
    # connecting the lines. Also returns the distance between the lines.

    c = np.cross(n1, n2)
    c1 = np.cross(n1, c)
    c2 = np.cross(n2, c)

    p1 = r1 + np.dot(r2 - r1, c2)/np.dot(n1, c2)*n1
    p2 = r2 + np.dot(r1 - r2, c1)/np.dot(n2, c1)*n2

    p = (p1 + p2)/2
    d = np.linalg.norm(p1 - p2)

    return p, d

def find_trajectory(vid_L, vid_R, cam_L, cam_R):

    # Finds the spatial location of the object as the intersection between the
    # lines drawn from each camera in the direction where the object appears in
    # that camera's frame.

    angles_L = get_angles(cam_L, vid_L)
    angles_R = get_angles(cam_R, vid_R)
    r1 = cam_L.pos
    r2 = cam_R.pos

    pts = np.array([[0, 0, 0]])
    dist = np.array(0)

    for a1, a2 in zip(angles_L, angles_R):

        n1 = direction(a1)
        n2 = direction(a2)
        p, d = intersection(r1, r2, n1, n2)

        pts = np.append(pts, [p], axis=0)
        dist = np.append(dist, d)

    pts = pts[1:, :]
    dist = dist[1:]

    return pts, dist
