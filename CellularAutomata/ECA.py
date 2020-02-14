"""
Created on Fri Jul 19 21:21:26 2019

@author: Steven Belcher (stevellen)
EVA functions for use in Boolean Networks course University of Nebraska Omaha
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation


def generate_ca(ru=np.random.randint(1, 256), it=250, n=51, k=1, **kwargs):
    """
        Cellular automata generator designed to create plots for rules in the range
        [1,255] with any number of iterations by default but is generalized and 
        can create rules up to 2^2k+1 for some value of k, which can be passed 
        as an argument to the function. 

        Additional argument options include:
            rand[bool] - If true, creates a random first generation;
            col[pair of str] - two color choices to indicate [dead, alive] cells,
            random_parents[bool] - determines if random parents are to be chosen 
                                when building a new generation;
            save[bool] - flag to indicate if the image should be saved;
            filename[str] - self explanatory.
    """
    # Assign default values to optional arguments
    rand = False
    random_parents = False
    col = ['white', 'black']
    save = False
    filename = 'eca.png'

    # Checking kwargs
    if 'rand' in kwargs:
        rand = kwargs['rand']
    if 'col' in kwargs:
        col = kwargs['col']
    if 'random_parents' in kwargs:
        random_parents = kwargs['random_parents']
    if 'save' in kwargs:
        save = kwargs['save']
    if 'filename' in kwargs:
        if kwargs['filename'][-4:] == '.png' or kwargs['filename'][-4:] == '.jpg':
            filename = kwargs['filename']
        else:
            filename = kwargs['filename'] + '.png'
    

    density = np.zeros(it)
    rows = np.zeros((it, n), dtype=int)
    assert rows is not None, "Number of nodes (n) and number of iterations (it) must be defined to build matrix."

    def __get_rule():
        out = format(ru, f'0{2**(2*k+1)}b')
        return {format(2**(2*k+1)-1-i, f'0{2*k+1}b'): int(out[i]) for i in range(2**(2*k+1))}

    def __plot_automaton():
        col_map = colors.ListedColormap(col)
        plt.figure(figsize=(16, 7))
        ax = plt.subplot(2, 1, 1)
        ax.set_title("ECA Rule {:,}".format(ru), fontsize=20)
        ax.set_ylabel("Nodes")
        plt.matshow(rows.T, cmap=col_map, interpolation='nearest',
                    aspect='auto', fignum=False)
        ax.xaxis.set_ticks_position('bottom')
        ax = plt.subplot(2, 1, 2)
        ax.set_title('Iterations')
        ax.set_ylabel("Density")
        plt.plot(np.arange(0, it, 1), density)
        plt.xlabel(f'Mean Density {np.round(np.mean(density), 3)}')
        
        if save:
            fig = plt.gcf()
            fig.savefig(filename)
        plt.show()

    def __apply_rule():
        fr = np.zeros(n, dtype=int)                    # Create first row
        if rand:
            fr = np.random.randint(0, 2, n)
        else:
            fr[n//2] = 1
        rows[0] = pr = fr                               # previous row
        nr = np.zeros(n, dtype=int)                     # next row
        rule = __get_rule()                             # fetch rule dict

        for i in range(1, it):                          # Need to find a cleaner way to do this
            density[i-1] = np.mean(rows[i-1])
            for j in range(n):
                if random_parents:
                    nc = pr[np.random.randint(0,n,2*k+1)]
                else:
                    if j - k < 0:
                        nc = np.concatenate([pr[j-k:], pr[:j+k+1]])
                    elif j + k >= n:
                        nc = np.concatenate([pr[j-k:], pr[:(k+j-n+1)]])
                    else:
                        nc = pr[j-k:j+k+1]
                r = ''.join([str(v) for v in nc])
                nr[j] = rule[r]
            pr = np.copy(nr)
            rows[i] = np.copy(nr)
        density[-1] = np.mean(rows[-1])

    __apply_rule()
    __plot_automaton()


def game_of_life(n=30, it=50, col=['black', 'white'], show=True, save=False):
    """
        The game_of_life function is a quick numpy implementation of Conway's game of life.
        The function takes the grid length and number of iterations as arguments and produces
        an animation for as long as the window remains open. If shown, the game will continue until 
        the window is closed. If saved, a file is generated in the CWD named 'life.mp4'.
    """
    try:
        n = int(n)
        it = int(it)
    except Exception as e:
        print(e)

    def __iterate(framenum, img, world, n):
        """ Perform animation iteration; returns an Artist. """
        grid = np.copy(world)
        for i in range(1, n+1):
            for j in range(1, n+1):
                window = world[i-1:i+2, j-1:j+2]
                total = np.sum(window)
                if world[i, j] == 1:    # Live cell case
                    if total-1 not in [2, 3]:
                        grid[i, j] = 0
                else:                  # Cell is dead
                    if total == 3:
                        grid[i, j] = 1
        img.set_array(grid)
        world[:, :] = grid[:, :]
        return img,

    """ Play the game of life """
    col_map = colors.ListedColormap(col)
    world = np.zeros((n+2, n+2), dtype=np.uint8)  # Generate empty world
    adam, eve = np.random.randint(
        1, n, n**2//10), np.random.randint(1, n, n**2//10)  # sow the seeds of life
    world[adam, eve] = 1
    fig = plt.figure(figsize=(8, 8))             # assign figure
    # assign image (Artist)
    im = plt.imshow(world, cmap=col_map, animated=True)
    anim = animation.FuncAnimation(fig, __iterate, fargs=(
        im, world, n), frames=it, interval=50, blit=True)

    if save:
        show = False
        anim.save('life.mp4', fps=25)
    if show:
        plt.show()
    plt.close()


if __name__ == "__main__":
    """ A quick, simple demo for if the file is called directly """
    rule = np.random.randint(1, 256)
    generate_ca(ru=rule, n=51, k=1, it=200, col=['yellow', 'black'])
    generate_ca(ru=rule, n=51, k=1, it=200, col=['yellow', 'black'], random_parents=True)
    # game_of_life(60)
