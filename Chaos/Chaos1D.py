"""
Credit for cobweb_plot to: Christian @ https://scipython.com/blog/author/christian/
Modified by: Steven Belcher
University of Nebraska Omaha
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import ArtistAnimation



def bifurcation_plot(f=lambda x,a: a*x*(1-x), n_points=200, a_step=0.01, iterations=100, animate=True):
    a_list = np.arange(1,4,a_step)
    x_in = np.linspace(0,1,n_points)
    x_out = np.empty((a_list.shape[0], ))
    fig = plt.figure(figsize=(10,7))
    artists = [[]]
    for idx,a in enumerate(a_list):
        x = np.copy(x_in)
        for _ in range(iterations):
            x = f(x,a)
        im = plt.plot(np.repeat(a,x.shape[0]), x, color='blue', 
                        marker='o', ls='', markersize=1)
        artists.append(artists[idx]+im)
    if animate:
        anim = ArtistAnimation(fig, artists, interval=1, repeat=False)
    plt.show()


def plot_logistic_iteration(f, a, k):
    x = np.linspace(0, 1, 300)
    y = f(x, a)
    square = np.sqrt(k)
    # Ensure square is an integer with
    if not square.is_integer():
        square = int(square)+1
    else:
        square = int(square)

    fig = plt.figure(figsize=(12, 7), dpi=100)
    fig.suptitle(f'Generated {k} iterations for a = {a}')
    for i in range(1, k+1):
        ax = fig.add_subplot(square, square, i)
        ax.plot(x, y)
        ax.plot(x, x, 'r')
        ax.grid(which='both', alpha=0.5)
        y = f(y, a)
    mngr = plt.get_current_fig_manager()
    mngr.set_window_title('Iteration Plots')
    # to put it into the upper left corner for example:
    plt.show()


def cobweb_plot(f, a, x0, k=40, show=True, save=False, filename='cobweb.png'):
    """
    Make a cobweb plot.

    Plot y = f(x; r) and y = x for 0 <= x <= 1, and illustrate the behaviour of
    iterating x = f(x) starting at x = x0. r is a parameter to the function.

    """
    # Make sure k is a float
    a = float(a)
    # Double k for plot generation. Array of length k is returned
    k *= 2
    x = np.linspace(0, 1, 500)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)

    # Plot y = f(x) and y = x
    ax.plot(x, f(x, a), c='#444444', lw=2)
    ax.plot(x, x, c='#444444', lw=2)

    # Iterate x = f(x) for k steps, starting at (x0, 0).
    px, py = np.empty((2, k+1))
    px[0], py[0] = x0, 0
    for n in range(1, k, 2):
        px[n] = px[n-1]
        py[n] = f(px[n-1], a)
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
    ax.set_title('$x_0 = {:.1}, a = {:.2}$'.format(x0, a))
    # plt.axis([0, 1, 0, 1])
    if save:
        fig = plt.gcf()
        fig.savefig(filename)
    if show:
        plt.show()

    return px[range(0, k+1, 2)]


if __name__ == "__main__":
    # Define a simple logistic map example
    def f(x, a): return a*x*(1-x)
    x0 = np.random.rand()
    a = np.random.rand()*3+1
    k = 11
    plot_logistic_iteration(f, a, k)
    k = 100
    cobweb_plot(f, a, x0, k)
    bifurcation_plot()