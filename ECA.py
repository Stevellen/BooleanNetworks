"""
Created on Fri Jul 19 21:21:26 2019

@author: Steven Belcher (stevellen)
ECA generator object for use in Boolean Networks course University of Nebraska Omaha
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation

class ECA:
    """
        This class implements elementary cellular automatons with two colors and
        three parent nodes. The constructor for this class takes three arguments,
        the number of Nodes in each row, the number of iterations to run and the
        number of the rule to be applied.

    """
    def __init__(self, n=None, it=None, k=1, ru=None, rand=False, col=['white', 'black']):
        self.n = n
        self.it = it
        self.k = k
        self.ru = ru
        self.rand = rand
        self.col = col
        self.rows = None
        self.density = np.zeros(it) if self.it else None
        self.rows = np.zeros((self.it, self.n), dtype=int) if (self.it and self.n) else None 

    def generate(self, save=False, n=None, it=None, k=1, ru=None, rand=False, col=['white', 'black']):
        self.k = k
        self.ru = ru
        self.it = it
        self.n = n
        self.rand = rand
        self.col = col
        if self.n and self.it:
            self.density = np.zeros(self.it)
            self.rows = np.zeros((self.it, self.n), dtype=int)
        assert self.rows is not None, "Number of nodes (n) and number of iterations (it) must be defined to build matrix."
        
        def __get_rule(r):
            out = format(r, f'0{2**(2*self.k+1)}b')
            return {format(2**(2*self.k+1)-1-i, f'0{2*self.k+1}b'):int(out[i]) for i in range(2**(2*self.k+1))}

        def __plot_automaton(dims = (16,7), save = False, filename = "eca.png"):
            col_map = colors.ListedColormap(self.col)
            plt.figure(figsize=dims)
            ax = plt.subplot(2,1,1)
            ax.set_title("ECA Rule {:,}".format(self.ru), fontsize=20)
            ax.set_ylabel("Nodes")
            plt.matshow(self.rows.T, cmap = col_map, interpolation='nearest', aspect='auto', fignum=False)
            ax.xaxis.set_ticks_position('bottom')
            ax = plt.subplot(2,1,2)
            ax.set_title('Iterations')
            ax.set_ylabel("Density")
            plt.plot(np.arange(0, self.it, 1), self.density)
            plt.xlabel(f'Mean Density {np.round(np.mean(self.density), 3)}')
            if save:
                plt.savefig(filename)
            plt.show()
            plt.close()

        def __apply_rule():
            fr = np.zeros(self.n, dtype=int)                    # Create first row
            if self.rand:
                fr = np.random.random_integers(0,1,self.n)
            else:
                fr[self.n//2] = 1
            self.rows[0] = pr = fr                              # previous row
            nr = np.zeros(self.n, dtype = int)                  # next row
            rule = __get_rule(self.ru)                     # fetch rule dict

            for i in range(1, self.it):                         # Need to find a cleaner way to do this
                self.density[i-1] = np.mean(self.rows[i-1])
                for j in range(self.n):
                    if j - self.k < 0:
                        # print(np.concatenate([pr[j-self.k:], pr[:j+self.k+1]]))
                        nc = np.concatenate([pr[j-self.k:], pr[:j+self.k+1]])
                    elif j + self.k >= self.n:
                        nc = np.concatenate([pr[j-self.k:], pr[:(self.k+j-self.n+1)]])
                    else:
                        # print(pr[j-self.k:j+self.k+1])
                        nc = pr[j-self.k:j+self.k+1]
                    r = ''.join([str(v) for v in nc])
                    nr[j] = rule[r]
                pr = np.copy(nr)
                self.rows[i] = np.copy(nr)
            self.density[-1] = np.mean(self.rows[-1])

        def __err_check():
            err_msg = "ECA generation requires {} to be defined with valid values.\n"
            err_details = []
            if self.n == None:
                err_details.append("number of nodes (n)")
            if self.it == None:
                err_details.append("iterations (it)")
            if self.ru == None:
                err_details.append("rule (ru)")
            if err_details:
                raise Exception(err_msg.format(', '.join(err_details)))

            if type(self.n) is not int or self.n <= 0:
                raise Exception("Number of nodes (N) must be a positive integer.")
            if type(self.it) is not int or self.it <= 0:
                raise Exception("Number of iterations (it) must be a positive integer.")
            if type(self.ru) is not int or self.ru < 0 or self.ru > 2**2**(2*self.k+1):
                raise Exception(f"Rule (ru) must be an integer in range [0,{2**2**(2*self.k+1)}].")
            if type(self.rand) is not bool:
                raise Exception("Parameter 'rand' must be of type bool.")

        __err_check()
        __apply_rule()
        __plot_automaton(save=save, filename='test.png')

if __name__ == "__main__":
    e = ECA()
    e.generate(save=True, k=3, n=101, it=500, ru=126345615885, rand=True)
    # e.game_of_life()