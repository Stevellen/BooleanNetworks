# Elementary Cellular Automata (and their generalizations)
### Steven Belcher
#### University of Nebraska Omaha

This document is a demo of the most current state of the ECA package. It will be updated whenever new functionality is added or old functionality modified. I will keep this header as a running log of the significant updates.

01/06/2020 - Refactoring of the old ECA script to be more efficient and produce better looking plots. Additional parameters were added to the $\textbf{generate()}$ function call so that a user may save the image, alter colors and select a larger window of parent cells. This allows for exploration of more generalized cellular automata and their patterns. 

First, we import the ECA package, as below.


```python
import ECA
```

Then it is a simple matter to create any sort of basic cellular automata by using the generate() function. This function has several arguments to specify a variety of options, including:
###### - number of iterations(it [int]), 
###### - number of nodes (n [int]), 
###### - size of parent window - calculated as 2k+1 (k=1 [int] by default), 
###### - random first row? [bool] (rand=False by default), 
###### - colors [list of string] to use in the plot (col=['white', 'black'] by default),
###### - whether to save the figure [bool] (save=False by default),
###### - filename to save to [string] (filename='eca.png by default),
###### - whether to show the generated plot [bool] (show=True by default).

The generate function has the signature:


<font size=2.5> ```generate(it=None, n=None, ru=None, rand=False, col=['white', 'black'], save=False, filename=eca.png, show=True) ```</font>



```python
ECA.generate(it=200, n=31, ru=94)
```


![png](/images/output_4_0.png)


When generate is called from the interpreter, a separate window opens that allows the user to zoom in and reposition the plots. Additionally, more general cellular automata can be produced by adjusting the value of k, broadening the window of parent cells and increasing the number of options for rules to $2^{2k+1}$ options.


```python
ECA.generate(it=200, n=31, ru=94, k=2)
```


![png](/images/output_6_0.png)


We see that even using the same set of rules, the increase in parent window leads to an increase in the number of rules and thus drastically alters the nature of the automata. We can look at some of the higher-order rules to see what it's like outside the original [0-255] range.


```python
ECA.generate(it=200, n=31, ru=25767, k=2)
```


![png](/images/output_8_0.png)


Of course we can also just randomize the first row to see how it disrupts the pattern.


```python
ECA.generate(it=200, n=31, ru=25767, k=2, rand=True)
```


![png](/images/output_10_0.png)


And of course you have to have the color options


```python
ECA.generate(it=200, n=31, ru=25767, k=2, col=['purple', 'silver'])
```


![png](/images/output_12_0.png)


The benefit of this module is that it is possible to do a very large number of nodes iterations very quickly when compared with the existing MATLAB script. We'll time the operation for good measure.


```python
from time import time
start = time()
ECA.generate(it=250, n=101, ru=8991354, k=2)
print(f'Finished in {time()-start} seconds on a 7 year old i5 processor.')
```


![png](/images/output_14_0.png)


    Finished in 0.4118633270263672 seconds on a 7 year old i5 processor.
    

Of course resolution becomed a problem as the numbers get bigger, but again, the interpreter will pop up a window that allows zooming and moving around. Just for fun, let's time a REALLY big one.


```python
start = time()
ECA.generate(it=5000, n=1001, ru=8991354, k=2)
print(f'Finished in {time()-start} seconds on a 7 year old i5 processor.')
```


![png](/images/output_16_0.png)


    Finished in 30.33807611465454 seconds on a 7 year old i5 processor.
    

Okay, so really big number still take a bit, but this same number of nodes and iterations took over 3 hours to run with the PatternFormation_Densityof1_generalizedRule22.m script on the same hardware, so the improvement is significant. Besides, plots of this resolution are far from necessary to observe the patterns (or lack thereof) in a given cellular automaton. Finally, we will plot a few random, normal-sized ones just for fun.


```python
import sys
import numpy as np
for rule in np.random.randint(np.iinfo(np.int32).max,size=10):
    ECA.generate(it=200, n=31, ru=rule, k=3)
```


![png](/images/output_18_0.png)



![png](/images/output_18_1.png)



![png](/images/output_18_2.png)



![png](/images/output_18_3.png)



![png](/images/output_18_4.png)



![png](/images/output_18_5.png)



![png](/images/output_18_6.png)



![png](/images/output_18_7.png)



![png](/images/output_18_8.png)



![png](/images/output_18_9.png)


# Game of Life
## Under Construction (Coming Soon)

