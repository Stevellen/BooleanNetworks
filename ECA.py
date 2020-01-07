"""
Created on Fri Jul 19 21:21:26 2019

@author: Steven Belcher (stevellen)
ECA generator object for use in Boolean Networks course University of Nebraska Omaha
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def generate(it=None, n=None, k=1, ru=None, rand=False, col=['white', 'black'], save=False, filename='eca.png', show=True):
        if n and it:
            density = np.zeros(it)
            rows = np.zeros((it, n), dtype=int)
        assert rows is not None, "Number of nodes (n) and number of iterations (it) must be defined to build matrix."
        
        def __get_rule():
            out = format(ru, f'0{2**(2*k+1)}b')
            return {format(2**(2*k+1)-1-i, f'0{2*k+1}b'):int(out[i]) for i in range(2**(2*k+1))}

        def __plot_automaton():
            col_map = colors.ListedColormap(col)
            plt.figure(figsize=(16,7))
            ax = plt.subplot(2,1,1)
            ax.set_title("ECA Rule {:,}".format(ru), fontsize=20)
            ax.set_ylabel("Nodes")
            plt.matshow(rows.T, cmap = col_map, interpolation='nearest', aspect='auto', fignum=False)
            ax.xaxis.set_ticks_position('bottom')
            ax = plt.subplot(2,1,2)
            ax.set_title('Iterations')
            ax.set_ylabel("Density")
            plt.plot(np.arange(0, it, 1), density)
            plt.xlabel(f'Mean Density {np.round(np.mean(density), 3)}')
            if save:
                plt.savefig(filename)
            if show:
                plt.show()
            plt.close()

        def __apply_rule():
            fr = np.zeros(n, dtype=int)                    # Create first row
            if rand: 
                fr = np.random.randint(0,2,n)
            else:
                fr[n//2] = 1
            rows[0] = pr = fr                              # previous row
            nr = np.zeros(n, dtype = int)                  # next row
            rule = __get_rule()                          # fetch rule dict

            for i in range(1, it):                         # Need to find a cleaner way to do this
                density[i-1] = np.mean(rows[i-1])
                for j in range(n):
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

        def __err_check():
            err_msg = "ECA generation requires {} to be defined with valid values.\n"
            err_details = []
            if n == None:
                err_details.append("number of nodes (n)")
            if it == None:
                err_details.append("iterations (it)")
            if ru == None:
                err_details.append("rule (ru)")
            if err_details:
                raise Exception(err_msg.format(', '.join(err_details)))

            if type(n) is not int or n <= 0:
                raise Exception("Number of nodes (N) must be a positive integer.")
            if type(it) is not int or it <= 0:
                raise Exception("Number of iterations (it) must be a positive integer.")
            if type(ru) not in [np.int32, np.int64, int]  or ru < 0 or ru > 2**2**(2*k+1):
                raise Exception(f"Rule (ru) must be an integer in range [0,{2**2**(2*k+1)}]. Given {ru}")
            if type(rand) is not bool:
                raise Exception("Parameter 'rand' must be of type bool.")

        __err_check()
        __apply_rule()
        __plot_automaton()

if __name__ == "__main__":
    generate(k=2, n=101, it=1000, ru=7500, rand=True)