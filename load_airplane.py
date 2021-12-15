from load_tarrain_color import custom_load_model
from load_tarrain_color import main
from mayavi import mlab
import numpy as np
from tvtk.api import tvtk

fig = mlab.figure(size=(1024, 1024))
main()

arr = np.genfromtxt("data/flight-coords.csv", delimiter=";")
arr = np.transpose(arr)

airplane_stl = custom_load_model('models/airplane2.stl')

airplane_mesh = mlab.triangular_mesh(airplane_stl[0], airplane_stl[1], airplane_stl[2], airplane_stl[3],
                     name='airplane', color=(1.0, 1.0, 1.0))
#tube = mlab.plot3d(arr[0], arr[1], arr[2], arr[5], tube_radius=4, line_width=0.3, name="Turbulence intensity")
#lut = tube.module_manager.scalar_lut_manager.lut.table.to_array()
#mlab.view(elevation=80, azimuth=5, focalpoint=(arr[0][500], arr[1][500], arr[2][500]), distance=1870)
#airplane_mesh.module_manager.scalar_lut_manager.lut.table = lut

scene = mlab.get_engine().scenes[0]
# for s in scene.children:
#     s.scene.disable_render = True
#scene.scene.movie_maker.record = True


def get_intensity(index: int) -> tuple:
    scale = 0.4
    # right = 0.04 * np.sin(d * 2) * turbulence_intensity * 0.01 * scale
    # up = - turbulence_intensity * 0.01 * scale
    up = - arr[6][index] * scale
    right = arr[3][index] * scale
    #intensity = turbulence_intensity * 0.01 * scale
    return up, right

@mlab.show
@mlab.animate(delay=16)
def anim():
    i = len(arr[0]) - 1
    tiltStart = 320
    tiltEnd = 215
    shakeDir = 1
    airplane_mesh.actor.actor.orientation = np.asarray((3, -0, 0))
    while 1:
        if i < tiltEnd:
            airplane_mesh.actor.actor.orientation = np.asarray((0, -0, 0))
        elif tiltStart > i > tiltEnd:
            factor = (tiltStart - i) / (tiltStart - tiltEnd)
            #print(factor)
            xelevation = 3 - (3 * factor)
            airplane_mesh.actor.actor.orientation = np.asarray((xelevation, -0, 0))

        airplane_mesh.actor.actor.position = (arr[0][i], arr[1][i], arr[2][i])
        pos = airplane_mesh.actor.actor.position
        mlab.view(elevation=80, azimuth=0, focalpoint=(pos[0], pos[1], pos[2]), distance=235)
        # turbulence shaking
        up, right = get_intensity(i)
        airplane_mesh.actor.actor.position = (pos[0] + (right * shakeDir), pos[1], pos[2] + (up * shakeDir))
        i -= 1
        shakeDir *= -1
        if i <= 0:
            return
        yield


anim()

