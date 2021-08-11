"""
networkmodels.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Tue Aug 10 22:14:22 CEST 2021

Contain Deep Learning models (mostly Multilayer perceptrons)

"""

impot torch
from torch import nn

class LRmodel(nn.Module):

    def __init__(self):
        """
        Linear Model 
        """
        super(LRmodel, self).__init__(in_layer, out_layer)
        self.layers = nn.Sequential(
            nn.Linear(), # input to hidden layer
            nn.ReLU(),
            nn.Linear() # output layer

        )

    def forward(self, x):
        """
        Forward pass

        Returns:
            torch.Tensor: model predictions
        """
        return self.layers(x)

