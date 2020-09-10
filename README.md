![minibrain](https://github.com/JoseGuzman/minibrain/workflows/minibrain/badge.svg)
[![Build Status](https://travis-ci.com/JoseGuzman/minibrain.svg?branch=master)](https://travis-ci.com/JoseGuzman/minibrain)
[![CodeFactor](https://www.codefactor.io/repository/github/joseguzman/minibrain/badge)](https://www.codefactor.io/repository/github/joseguzman/minibrain)

# minibrain 

A Python module to analyze electrical signals and calcium fluorescence in brain organoids. For personal use only.

## Requirements

The module has been extensively tested on Python >= 3.5. We recommend to have a package manager like Anaconda with:
1. Standard scientific modules for data handling ([IPython and Jupyter](https://ipython.org/) , [pandas](https://pandas.pydata.org/)), 
2. Modules for scientific analysis ([Scipy](https://scipy.org/), [NumPy](https://numpy.org/) and machine learning ([Scikit-learn](https://scikit-learn.org/)) 
3. The scientific library for data visualization ([matplotlib](https://matplotlib.org/)). 

Assuming that you do not have an environment already, you can create it and download [minibrain.yml](https://github.com/JoseGuzman/minibrain/blob/master/minibrain.yml) and type:

```bash
conda create -n minibrain -f minibrain.yml
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

* [Calculate Bursts](https://github.com/JoseGuzman/minibrain/wiki/Calculate-Burst)

## License
Minibrain is free software. You can redistribute it and modify it under the terms of the GNU General Public License (GPL).   either version 2 of the License, or any later version as published by the Free Software Foundation.

Minibrain is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
