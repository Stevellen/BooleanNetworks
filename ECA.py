# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 21:21:26 2019

@author: Steven Belcher (stevellen)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class ECA:
    """
        This class implements elementary cellular automatons with two colors and
        three parent nodes. The constructor for this class takes three arguments,
        the number of Nodes in each row, the number of iterations to run and the
        number of the rule to be applied.

    """
    def __init__(self, N=None, it=None, ru=None, rand=False, col=['white', 'black']):
        self.N = N
        self.it = it
        self.ru = ru
        self.rand = rand
        self.col = col
        self.rows = None
        if self.it and self.N:
            self.rows = np.zeros((self.it, self.N), dtype=int)

    def get_rule(self, r):
        out = '{:08b}'.format(r)
        return {format(7-i, '03b'):int(out[i]) for i in range(8)}

    def plot(self):
        self.plot_automaton()

    def plot_automaton(self, col = ['white', 'black'], dims = (12,8), save = False, filename = "eca.png"):
        col_map = colors.ListedColormap(["white", "black"])
        plt.figure(figsize=dims)
        plt.imshow(self.rows, cmap = col_map, interpolation='nearest')
        plt.xlabel("Nodes")
        plt.ylabel("Iterations")
        plt.title("ECA Rule {}".format(self.ru))
        plt.savefig(filename)
        plt.show()
        plt.close()

    def apply_rule(self):
        fr = np.zeros(self.N, dtype=int)                    # Create first row
        if self.rand:
            fr = None
        else:
            fr[self.N//2] = 1


        self.rows[0] = pr = fr                              # previous row
        nr = np.zeros(self.N, dtype = int)                  # next row
        rule = self.get_rule(self.ru)                       # fetch rule dict

        for i in range(1, self.it):
            for j in range(self.N):
                if j == 0:
                    nc = [pr[-1], pr[0], pr[1]]
                elif j == self.N-1:
                    nc = [pr[-2], pr[-1], pr[0]]
                else:
                    nc = pr[j-1:j+2]
                r = ''.join([str(v) for v in nc])
                nr[j] = rule[r]
            pr = np.copy(nr)
            self.rows[i] = np.copy(nr)

    def err_check(self):
        err_msg = "ECA generation requires properties {} to be defined with valid values.\n"
        err_details = []
        if self.N == None:
            err_details.append("N")
        if self.it == None:
            err_details.append("it")
        if self.ru == None:
            err_details.append("ru")
        if err_details:
            raise Exception(err_msg.format(', '.join(err_details)))

        if type(self.N) is not int or self.N <= 0:
            raise Exception("Number of nodes (N) must be a positive integer.")
        if type(self.it) is not int or self.it <= 0:
            raise Exception("Number of iterations (it) must be a positive integer.")
        if type(self.ru) is not int or self.ru < 0 or self.ru > 255:
            raise Exception("Rule (ru) must be an integer in range [0,255].")
        if type(self.rand) is not bool:
            raise Exception("Parameter 'rand' must be of type bool.")

    def clear_params(self):
        self.it = None
        self.N = None
        self.ru = None
        self.rows = None
        self.rand = False

    def generate(self, **kwargs):
        if kwargs:
            accept = kwargs.keys()
            if 'ru' in accept:
                self.ru = kwargs['ru']
            if 'it' in accept:
                self.it = kwargs['it']
            if 'N' in accept:
                self.N = kwargs['N']
            if 'rand' in accept:
                self.rand = kwargs['rand']
            if 'col' in accept:
                self.col = kwargs['col']
            if self.N and self.it:
                self.rows = np.zeros((self.it, self.N), dtype=int)
            assert self.rows is not None, "Number of nodes (N) and number of iterations (it) must be defined to build matrix."

        self.err_check()
        self.apply_rule()
        self.plot_automaton()
