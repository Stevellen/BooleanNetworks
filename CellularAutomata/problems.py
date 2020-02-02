import ECA
import pandas as pd
from Chaos import cobweb_plot


def f(x, k): return k*x*(1-x)


fx, fy = cobweb_plot(f, 3.5, 0.1)
df = pd.DataFrame({'n': range(len(fx)), 'f(n)(x)': fx, 'f(n+1)(x)': fy})
# more options can be specified also
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)
