import numpy as np
from mayavi import mlab
from stl import mesh


def custom_load_model(filename):
    model = mesh.Mesh.from_file(filename)
    x = model.x.flatten()
    y = model.y.flatten()
    z = model.z.flatten()
    t = [(0. + i * 3., 1. + i * 3., 2. + i * 3.) for i
         in range(0, int(x.size/3))]
    return x, y, z, t


def main():
    arr = np.genfromtxt("data/flight-coords.csv", delimiter=";")
    arr = np.transpose(arr)
    #fig = mlab.figure(size=(1024, 1024))

    tube1 = mlab.plot3d(arr[0], arr[1], arr[2], arr[3], tube_radius=4, line_width=0.3, name="cw Speed deficit change")
    # tube2 = mlab.plot3d(arr[0], arr[1], arr[2], arr[4], tube_radius=4, line_width=0.3, name="Crosswind velocity")
    # tube2 = mlab.plot3d(arr[0], arr[1], arr[2], arr[7], tube_radius=4, line_width=0.3, name="Tailwind velocity")
    # tube2 = mlab.plot3d(arr[0], arr[1], arr[2], arr[6], tube_radius=4, line_width=0.3, name="Tailwind change")
    # tube3 = mlab.plot3d(arr[0], arr[1], arr[2], arr[5], tube_radius=4, line_width=0.3, name="Turbulence intensity")

    terrain = custom_load_model('models/terreng.stl')

    terrain_large = custom_load_model('models/terreng_stort.stl')

    building_main = custom_load_model('models/hovedbygg.stl')

    building_other = custom_load_model('models/nabobygg.stl')

    mlab.triangular_mesh(building_main[0], building_main[1], building_main[2], building_main[3], color=(0.9, 0.4, 0.3), name='New building')

    mlab.triangular_mesh(building_other[0], building_other[1], building_other[2], building_other[3], color=(0.5, 0.5, 0.5), name='Old buildings')

    surf1 = mlab.triangular_mesh(terrain[0], terrain[1], terrain[2], terrain[3], vmin=-73., vmax=73.,
                                 name='Terrain fine detail', colormap='ocean')

    surf1.module_manager.scalar_lut_manager.load_lut_from_file('misc/custom-ocean.lut')

    surf2 = mlab.triangular_mesh(terrain_large[0], terrain_large[1], terrain_large[2], terrain_large[3], vmin=-73., vmax=74.,
                                 name='Terrain large', colormap='ocean')

    surf2.module_manager.scalar_lut_manager.load_lut_from_file('misc/custom-ocean.lut')

    #airplane = custom_load_model('models/Airbus_A380_Final_V.stl')

    # mlab.triangular_mesh(airplane[0], airplane[1], airplane[2], airplane[3], color=(0.8, 0.8, 0.8),
    #                      name='airplane')
    #mlab.show()


#main()