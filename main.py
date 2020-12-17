from utils.trajectory import find_trajectory, direction
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class camera:
    def __init__(self, position, direction, view_angles):
        # Attributes: Spatial location of the camera, the direction in which
        # the camera is facing, and the angular size of the camera's view
        self.pos = np.array(position)
        self.dir = np.pi/180*np.array(direction)
        self.view = np.pi/180*np.array(view_angles)

cam_L = camera([0, 0, 0.128], [0, 0], [55.9, 33.0])
cam_R = camera([1, 0, 0.116], [0, -45], [52.3, 30.1])

vid_L = 'left.mp4'
vid_R = 'right.mp4'

pts, dist = find_trajectory(vid_L, vid_R, cam_L, cam_R)

# Now we plot a beautiful animation of the computed trajectory

# https://stackoverflow.com/questions/16488182/removing-axes-margins-in-3d-plot
""" patch start """
from mpl_toolkits.mplot3d.axis3d import Axis
if not hasattr(Axis, "_get_coord_info_old"):
    def _get_coord_info_new(self, renderer):
        mins, maxs, centers, deltas, tc, highs = self._get_coord_info_old(renderer)
        mins += deltas / 4
        maxs -= deltas / 4
        return mins, maxs, centers, deltas, tc, highs
    Axis._get_coord_info_old = Axis._get_coord_info
    Axis._get_coord_info = _get_coord_info_new
""" patch end """

fig = plt.figure(figsize = (7.2, 7.2))
ax = fig.add_subplot(111, projection='3d')

x_min = -0.5
x_max = 1.5
y_min = 0
y_max = 2
z_min = 0
z_max = 1

ax.set_xlim3d(x_min, x_max)
ax.set_ylim3d(y_min, y_max)
ax.set_zlim3d(z_min, z_max)

x_L, y_L, z_L = cam_L.pos
x_R, y_R, z_R = cam_R.pos

# Position of the two cameras
ax.scatter([x_L], [y_L], [z_L], color='k', s=50)
ax.scatter([x_R], [y_R], [z_R], color='k', s=50)

# Lines from each camera in the direction the camera is facing
n_L = direction(cam_L.dir)
ax.plot([x_L, x_L + 2*n_L[0]],
        [y_L, y_L + 2*n_L[1]],
        [z_L, z_L + 2*n_L[2]],
        'b-', linewidth=1)

n_R = direction(cam_R.dir)
ax.plot([x_R, x_R + 2*n_R[0]],
        [y_R, y_R + 2*n_R[1]],
        [z_R, z_R + 2*n_R[2]],
        'r-', linewidth=1)

N = len(pts)
P = np.zeros((N, 3))

i = -1
for p in pts:
    i = i+1
    P[i, :] = p

data = [np.zeros((3, N))]

for i in range(N):
    data[0][:, i] = P[i]

def update(n, data, draw):
    for draw, data in zip(draw, data):
        draw.set_data(data[0:2, :n])
        draw.set_3d_properties(data[2, :n])
    return draw

draw = [ax.plot(data[0][0, 0:0], data[0][1, 0:0], data[0][2, 0:0],
                linewidth = 3, color = 'orange')[0]]

# The hack for removing margins spoils the x-axis, so we draw it again 
ax.plot([x_min, x_max], [y_min, y_min], [z_min, z_min], color='k', linewidth=0.5)

ani = FuncAnimation(fig, update, N+1, fargs = (data, draw),
                    interval = 33.33, repeat_delay = 1000)

plt.show()
