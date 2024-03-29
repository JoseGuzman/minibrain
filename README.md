# minibrain ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/JoseGuzman/minibrain) 

 
 
[![Build Status](https://app.travis-ci.com/JoseGuzman/minibrain.svg?branch=master)](https://app.travis-ci.com/JoseGuzman/minibrain)
[![CodeFactor](https://www.codefactor.io/repository/github/joseguzman/minibrain/badge)](https://www.codefactor.io/repository/github/joseguzman/minibrain) [![GitHub license](https://img.shields.io/github/license/JoseGuzman/minibrain)](https://github.com/JoseGuzman/minibrain/blob/master/LICENSE) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJoseGuzman%2Fminibrain&count_bg=%233DC8C7&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=views&edge_flat=false)](https://hits.seeyoufarm.com)


![minibrain](https://github.com/JoseGuzman/minibrain/blob/master/misc/img/spikes.png)

A Python module to analyze electrical signals and calcium fluorescence in brain organoids. For personal use only.



## Requirements

The module has been extensively tested on Python >= 3.6. We recommend to have a package manager like Anaconda with:
1. Standard scientific modules for data handling ([IPython and Jupyter](https://ipython.org/) , [pandas](https://pandas.pydata.org/)), 
2. Modules for scientific analysis ([Scipy](https://scipy.org/), [NumPy](https://numpy.org/) and machine learning [Scikit-learn](https://scikit-learn.org/)) 
3. The scientific library for data visualization ([matplotlib](https://matplotlib.org/)). 
4. Deep Learning platform ([PyTorch](https://pytorch.org))

You can create a conda environment with necessary packages with the following command

```bash
conda env create --name minibrain --file environment.yml
```

## How to install it

If you prefer installing directly the minibrain package in one of your environments, just type this:

```bash
git clone https://github.com/JoseGuzman/minibrain.git
cd minibrain
pip install -r requirements.txt
pip install -e .
```

## Examples of usage

* [Calculate Bursts](https://github.com/JoseGuzman/minibrain/wiki/Calculate-Burst)

