import numpy as np
from mayavi import mlab
import random
from tvtk.tools import visual

arr = np.genfromtxt("data/flight-coords.csv", delimiter=";")
arr = np.transpose(arr)


# f = mlab.figure(size=(500,500))
# visual.set_viewer(f)


index = 2
@mlab.show
@mlab.animate(delay=10)
def anim():
    """Animate the b1 box."""
    print("start animation")
    i = 2
    while 1:
        if i < 775:
            mlab.view(elevation=87, azimuth=90, focalpoint=(arr[0][len(arr) - i], arr[1][len(arr) - i], arr[2][len(arr) - i]), distance=1)
        elif i > 785:
            mlab.view(elevation=90, azimuth=90, focalpoint=(arr[0][len(arr) - i], arr[1][len(arr) - i], arr[2][len(arr) - i]), distance=1)
        else:
            factor = (i - 775) / 10.0
            print(factor)
            el = 87 + (factor * 3)
            mlab.view(elevation=el, azimuth=90, focalpoint=(arr[0][len(arr) - i], arr[1][len(arr) - i], arr[2][len(arr) - i]), distance=1)

        print("i: {}, z: {}".format(i, arr[2][len(arr) - i]))

        intensity = arr[3][len(arr) - i]
        mlab.move(0, random.uniform(-1, 1) * intensity, random.randint(-1, 1) * intensity)

        i += 1
        if i > 1000:
            return
        yield



# Run the animation.
anim()


