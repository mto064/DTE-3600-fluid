import numpy as np
from mayavi import mlab
import mayavi
import random
from tvtk.tools import visual
import load_tarrain_color
from load_tarrain_color import custom_load_model

from data.vertices.a330_v_x import a330_v_x
from data.vertices.a330_v_y import a330_v_y
from data.vertices.a330_v_z import a330_v_z
from data.faces.a330_f import a330_f

arr = np.genfromtxt("data/flight-coords.csv", delimiter=";")
arr = np.transpose(arr)


# f = mlab.figure(size=(500,500))
# visual.set_viewer(f)
#f = mlab.figure()
fig = mlab.figure(size=(1024, 1024))
load_tarrain_color.main()

scene = mlab.get_engine().scenes[0]
scene.scene.movie_maker.record = True


# f.scene.movie_maker.record = True
# eng = mlab.get_engine()
# sc = eng.current_scene
# sc.movie_maker.record = True
for s in scene.children:
    s.scene.disable_render = True
showCockpit = True
cockpit = None
if showCockpit:
    cockpit_stl = custom_load_model('models/cockpit2.stl')
    cockpit = mlab.triangular_mesh(cockpit_stl[0], cockpit_stl[1], cockpit_stl[2], cockpit_stl[3], color=(0.7, 0.7, 0.7))


def get_intensity(index: int, d: float) -> tuple:
    scale = 1.5
    # right = 0.04 * np.sin(d * 2) * turbulence_intensity * 0.01 * scale
    # up = - turbulence_intensity * 0.01 * scale
    up = - arr[6][index] * scale
    right = arr[3][index] * scale
    #intensity = turbulence_intensity * 0.01 * scale
    return up, right


camera_elevation_offset = -5
camera_distance = 8

if showCockpit:
    cockpit.actor.actor.position = (arr[0][len(arr[0]) - 1], arr[1][len(arr[0]) - 1], arr[2][len(arr[0]) - 1])
    cockpit.actor.actor.orientation = np.asarray((3, 0, 0))
mlab.view(elevation=(87 + camera_elevation_offset), azimuth=90,
          focalpoint=(arr[0][len(arr[0]) - 1], arr[1][len(arr[0]) - 1], arr[2][len(arr[0]) - 1]), distance=camera_distance)

@mlab.show
@mlab.animate(delay=16)
def anim():
    # mlab.text(0.5, 0.5, "Test")
    v = 44
    dt = 0.016
    v_dt = v * dt
    d = 0
    print("start animation")
    i = len(arr[0]) - 1
    tiltStart = 320
    tiltEnd = 215
    shakeDir = 1
    planeElevation = 87 + camera_elevation_offset
    while 1:
        cockpit.actor.actor.position = (arr[0][i], arr[1][i], arr[2][i])
        if i > tiltStart:
            planeElevation = 87 + camera_elevation_offset
        elif i < tiltEnd:
            planeElevation = 90 + camera_elevation_offset
        else:
            factor = (tiltStart - i) / (tiltStart - tiltEnd)
            #print(factor)
            planeElevation = 87 + (factor * 3) + camera_elevation_offset
            if showCockpit:
                cockpit.actor.actor.orientation = np.asarray((3 - (factor * 3), 0, 0))
        if showCockpit:
            planePos = cockpit.actor.actor.position
            mlab.view(elevation=planeElevation, azimuth=90,
                      focalpoint=(planePos[0], planePos[1], planePos[2]), distance=camera_distance)


        up, right = get_intensity(i, d)
        # print(right)
        #mlab.move(0, random.uniform(-1, 1) * intensity, random.randint(-1, 1) * intensity)
        #mlab.move(0, (right * 10), (up * 10),)
        if showCockpit:
            planePos = cockpit.actor.actor.position
            cockpit.actor.actor.position = (planePos[0] + (right * shakeDir), planePos[1], planePos[2] + (up * shakeDir))
            planePos = cockpit.actor.actor.position
            mlab.view(elevation=planeElevation, azimuth=90,
                      focalpoint=(planePos[0], planePos[1], planePos[2]), distance=camera_distance)

        d += v_dt
        i -= 1
        shakeDir *= -1
        if i < 0:
            return
        yield



# Run the animation.
anim()
# mlab.show()

