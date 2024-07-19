import numpy as np
import matplotlib.pyplot as plt

def mandelbrot_set(c, max_iter):
    """
    Returns a 2D array representing the Mandelbrot set.
    c: complex number (x + yi)
    max_iter: maximum number of iterations to test for convergence
    """
    width, height = 800, 800
    img = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            z = complex(x / (width / 3.5), y * 2.0 / (height / 1.5) - 2)
            c_value = z
            for i in range(max_iter):
                if abs(z) > 2:
                    img[y, x] = i
                    break
                z = z ** 2 + c_value
        return img

# Example usage:
img = mandelbrot_set(complex(0.5, 0), 256)
plt.imshow(img, cmap='hot', interpolation='none')
plt.show()