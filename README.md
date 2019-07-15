# minibrain

A python module to analyze electrophysiology and calcium imaging in minibrains.

Requirements
============

We recommend to have a scientific Python distribution like Anaconda with the (NumPy, SciPy, matplotlib, IPython, Pandas). 

```bash
conda update -n base -c default conda 
```

* Python (tested in 2.7, will not work in Python 3.6)

How to install it
=================
To download and install the minibrain package:

```bash
git clone https://github.com/JoseGuzman/minibrain.git
cd minibrain
conda env create -n minibrain -f environment.yml
#pip install -r requirements.txt
pip install -e .
```

Basic usage
===========
In python:

```python
from minibrain import EphysLoader
```

