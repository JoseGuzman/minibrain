<a href="https://twitter.com/GuZman_Lab">
  <img align="left" alt="Jose's Twitter" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg" />
</a>
<a href="https://www.linkedin.com/in/sjmguzman/">
  <img align="left" alt="Jose's Linkdein" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />
</a>
<a href="https://github.com/JoseGuzman">
  <img align="left" alt="Jose's Github" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/github.svg" />
</a>
<a href="https://www.kaggle.com/joseguzman">
  <img align="left" alt="Jose's Kaggle" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/kaggle.svg" />
</a>

# minibrain

 ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/JoseGuzman/minibrain)  [![Build Status](https://travis-ci.com/JoseGuzman/minibrain.svg?branch=master)](https://travis-ci.com/JoseGuzman/minibrain) ![minibrain](https://github.com/JoseGuzman/minibrain/workflows/minibrain_unittest/badge.svg) [![CodeFactor](https://www.codefactor.io/repository/github/joseguzman/minibrain/badge)](https://www.codefactor.io/repository/github/joseguzman/minibrain)  [![GitHub license](https://img.shields.io/github/license/JoseGuzman/minibrain)](https://github.com/JoseGuzman/minibrain/blob/master/LICENSE) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJoseGuzman%2Fminibrain&count_bg=%233DC8C7&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=views&edge_flat=false)](https://hits.seeyoufarm.com)


![minibrain](https://github.com/JoseGuzman/minibrain/blob/master/img/spikes.png)

A Python module to analyze electrical signals and calcium fluorescence in brain organoids. For personal use only.



## Requirements

The module has been extensively tested on Python >= 3.5. We recommend to have a package manager like Anaconda with:
1. Standard scientific modules for data handling ([IPython and Jupyter](https://ipython.org/) , [pandas](https://pandas.pydata.org/)), 
2. Modules for scientific analysis ([Scipy](https://scipy.org/), [NumPy](https://numpy.org/) and machine learning [Scikit-learn](https://scikit-learn.org/)) 
3. The scientific library for data visualization ([matplotlib](https://matplotlib.org/)). 

You can create a conda environment with necessary packages

```bash
conda env create -f environment.yml
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
