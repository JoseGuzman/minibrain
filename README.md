# minibrain ![minibrain](https://github.com/JoseGuzman/minibrain/workflows/minibrain/badge.svg)

A python module to analyze electrophysiology and calcium imaging in minibrains.

Requirements
============
The module works only with Python3. We recommend to have a package manager like Anaconda with standard scientific modules for data handling (ipython, pandas), analysis (Scipy, NumPy, Scikit-learn) and visualization (matplotlib). Assuming that you do not have an environment already, you can create it and download [minibrain.yml](https://github.com/JoseGuzman/minibrain/blob/master/minibrain.yml) and type:

```bash
conda env create -n minibrain -f minibrain.yml
```

How to install it
=================
To download and install the minibrain package:

```bash
git clone https://github.com/JoseGuzman/minibrain.git
cd minibrain
pip install -r requirements.txt
pip install -e .
```

Basic usage
===========
In Python:

```python
from minibrain import EphysLoader
myrec = EphysLoader('continuous.dat')

from minibrain import Units
myunits = Units('/')
```

