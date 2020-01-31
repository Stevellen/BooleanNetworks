"""
Credit for cobweb_plot to: Christian @ https://scipython.com/blog/author/christian/
Modified by: Steven Belcher
University of Nebraska Omaha
"""

import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt


def cobweb_plot(f, k, x0, it=40, save=False, filename='cobweb.png'):
    """
    Make a cobweb plot.

    Plot y = f(x; r) and y = x for 0 <= x <= 1, and illustrate the behaviour of
    iterating x = f(x) starting at x = x0. r is a parameter to the function.

    """
    x = np.linspace(0, 1, 500)
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)

    # Plot y = f(x) and y = x
    ax.plot(x, f(x, k), c='#444444', lw=2)
    ax.plot(x, x, c='#444444', lw=2)

    # Iterate x = f(x) for it steps, starting at (x0, 0).
    px, py = np.empty((2,it+1,2))
    px[0], py[0] = x0, 0
    for n in range(1, it, 2):
        px[n] = px[n-1]
        py[n] = f(px[n-1], k)
        px[n+1] = py[n]
        py[n+1] = py[n]

    # Plot the path traced out by the iteration.
    ax.plot(px, py, c='b', alpha=0.7)
    
    # Annotate and tidy the plot.
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('$x$')

    # Avoid requiring passed functions to have attributes
    if not hasattr(f, 'label'):
        label = 'y'
    else:
        label = f.label

    ax.set_ylabel(label)
    ax.set_title('$x_0 = {:.1}, k = {:.2}$'.format(x0, k))
    plt.axis([0,1,0,1])
    if save:
        fig = plt.gcf()
        fig.savefig(filename)
    plt.show()
    


if __name__ == "__main__":
    # Define a simple logistic map example
    f = lambda x,k: k*x*(1-x)
    cobweb_plot(f, 3.1, 0.1, 100)