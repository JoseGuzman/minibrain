![minibrain](https://github.com/JoseGuzman/minibrain/workflows/minibrain/badge.svg)

# minibrain 

A Python module to analyze electrical signals and calcium fluorescence in brain organoids. For personal use only.

## Requirements

The module has been extensively tested on Python >3.5. We recommend to have a package manager like Anaconda with:
1. Standard scientific modules for data handling ([IPython and Jupyter](https://ipython.org/) , [pandas](https://pandas.pydata.org/)), 
2. Modules for scientific analysis ([Scipy](https://scipy.org/), [NumPy](https://numpy.org/) and machine learning ([Scikit-learn](https://scikit-learn.org/)) 
3. The scientific library for data visualization ([matplotlib](https://matplotlib.org/)). 

Assuming that you do not have an environment already, you can create it and download [minibrain.yml](https://github.com/JoseGuzman/minibrain/blob/master/minibrain.yml) and type:

```bash
conda env create -n minibrain -f minibrain.yml
```

## How to install it

To download and install the minibrain package:

```bash
git clone https://github.com/JoseGuzman/minibrain.git
cd minibrain
pip install -r requirements.txt
pip install -e .
```

## Examples of usage

(Calculate Burst)

 [[Link Text|nameofwikipage]]
In Python:

```python
from minibrain import EphysLoader
myrec = EphysLoader('continuous.dat')

from minibrain import Units
myunits = Units('/')

from minibrain.lfp import power
```

