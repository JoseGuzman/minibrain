"""
networkmodels.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Tue Aug 10 22:14:22 CEST 2021

Contain Deep Learning models
PyTorch inherits from  nn.Module and implement some important methods:

__init__: layers and activation functions will be used.

forward: It specifies the computations the network needs to do when data
is passed through it. We can use __call__ directly to invoke the forward method.

predict: to quickly get the most likely label from the network.
It calls the forward method and chooses the label with the highest score.

train: used to train the network parameters.

"""

impot torch
from torch import nn

class LRNet(nn.Module):
    """
    A linear Neural Net with zero hidden layers is very similar to a Linear
    regresion.
    """

    def __init__(self, in_dim:int, out_dim:int):
        """
        Linear Model
        """
        super(LRNet, self).__init__()
        # a linear layer has weights and bias values
        self.out = nn.Linear(in_dim, out_dim)

    def forward(self, x:torch.Tensor):
        """
        Forward pass to calculate prediction.

        Args:
            x (torch.Tensor): 1D tensor of features

        Returns:
            torch.Tensor: model prediction
        """
        y_pred = self.out(x)
        return y_pred

    def predict(self, x:torch.Tensor):
        """
        Model prediction
        """
        output = self.forward(x)
        return output

    def train(self, X, y):
        pass
