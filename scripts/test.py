"""
test.py

Jose Guzman, jose.guzman@guzman-lab.com
Fri Feb 18 21:52:57 CET 2022


Streamlit script to build the data app,
To test it run:
$> streamlit run scripts/test.py
"""

import streamlit as st

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('https://raw.githubusercontent.com/JoseGuzman/minibrain/master/minibrain/paper.mplstyle') 

from sklearn.decomposition import PCA
from minibrain.utils import mycolors

# Define main body
my_file = Path('./scripts/readme.md').read_text()
st.markdown(my_file, unsafe_allow_html=True)

left_col, right_col = st.columns(2)
left_col.subheader("PCA projection")
#middle_col.subheader("UMAP projection")
right_col.subheader("UMAP projection")

# Define sidebar
st.sidebar.title("Control Panel")
tissue = st.sidebar.radio("Select tissue", mycolors.keys())
st.sidebar.write('---')
k = st.sidebar.slider('Number of spike clusters',2,10,3)  #  
st.sidebar.write(k, 'squared is', k * k)

# Dimensionality reduction by PCA
@st.cache
def pca_reduction(n_components):
    """
    """
    mypath = './DataSets/waveforms.csv'
    waveforms = pd.read_csv(mypath, index_col = 'uid')
    df = waveforms.drop(['organoid'], axis = 1)
    trace = df.values[:, 30:] # remove first 30 samples (1 ms) of waveform baseline
    
    mypca = PCA(n_components)
    PC = mypca.fit_transform(trace)
    var = mypca.explained_variance_ratio_*100 # variance in percentage
    
    
    waveforms['PC1'] = PC[:,0]
    waveforms['PC2'] = PC[:,1]

    return (waveforms, var)


waveforms, var = pca_reduction(n_components = 2 )
# visualize
fig, ax = plt.subplots(1,1, figsize=(4,3))

ax.scatter(x = waveforms.PC1, y = waveforms.PC2, s=6, c='gray')
ax.set_xlabel(f'PC$_1$ = {var[0]:2.1f} %');
ax.set_ylabel(f'PC$_2$ = {var[1]:2.1f} %');
ax.set_xlim(-3,3); 
ax.set_ylim(-3,3);
ax.set_yticks([-2,0,2])
ax.set_xticks([-2,0,2])

left_col.pyplot(fig)
left_col.pyplot(fig)
right_col.pyplot(fig)
right_col.pyplot(fig)
#st.write(f'{waveforms.shape[0]} spikes')
st.markdown('*Check out this [article](https://www.kaggle.com/joseguzman/spike-classification-based-on-waveforms) for a detailed walk-through!*')