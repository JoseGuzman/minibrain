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

class MultipleRegression(nn.Module):
    """
    A linear Neural Net with zero hidden layers is very similar to a Linear
    regresion.
    """

    def __init__(self, n_weight:int):
        """
        Initializes a multiple variable regression of the form:

        y = X * w + b,

        where X is a matrix of observations x features, and w is a column
        vectors of weights. b is the bias term

        Args:
            n_weight (int): the number of weights
        """
        super(MultipleRegression, self).__init__()
        assert isinstance(n_weight, int)

        # note that w is a column vector of size (n,1), where n
        # is the number of independent variables.
        self.w = torch.randn( size = (n_weight, 1), dtype = torch.float,
            requires_grad = True)
        self.b = torch.rand(1,
            requires_grad = True)


    def forward(self, X:torch.Tensor):
        """
        Forward pass to calculate prediction following this form:

        y = X * w + b

        Args:
            X (torch.Tensor): 2D tensor of features

        Returns:
            torch.Tensor: model prediction
        """
        y_pred = X @ self.w + self.b
        return y_pred

    def train(self, X, y):
        pass
