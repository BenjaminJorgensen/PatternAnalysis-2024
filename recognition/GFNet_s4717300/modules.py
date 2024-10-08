## 1. “modules.py" containing the source code of the components of your model. Each component must be
# implemented as a class or a function
import torch
import torch.nn as nn
from torch.fft import fft2, ifft2

class GFNet(nn.Module):
    def __init__(self, dim, W, H, channels, num_classes=2) -> None:
        super().__init__()
        self.dim = dim
        self.width = W
        self.height = H
        self.num_classes = num_classes
        self.channels = channels

    def forward(self, x):
        pass


# NOTE: Maybe reshape the input before and after? - got it
# CONSIDER ADDING DROPOUT
class FeedFowardNetwork(nn.Module):
    def __init__(self, dim, W, H, act_layer=nn.LeakyReLU, norm_layer=nn.LayerNorm):
        super().__init__()
        self.dim = dim
        self.width = W
        self.height = H
        self.norm_layer = norm_layer
        self.act_layer = act_layer()
        self.fc1 = nn.Linear(dim, dim)
        self.fc2 = nn.Linear(dim, dim)

    def forward(self, x):
        x = self.norm_layer(x) # WARNING: This might be wrong - don't really know what norm_layer takes as input
        x = self.fc1(x)
        x = self.act_layer(x)
        x = self.norm_layer(x)
        x = self.fc2(x)
        x = self.act_layer(x)
        return x

class GlobalFilterLayer(nn.Module):
    def __init__(self, dim, h, w, norm_layer=nn.LayerNorm):
        self.dim = dim
        self.norm_layer = norm_layer
        self.complex_weight = nn.Parameter(torch.randn(h, w, dim, 2, dtype=torch.float32) * 0.02)
        super().__init__()

    def forward(self, x):
        B, H, W, C = x.shape
        x = torch.fft.rfft2(x, dim=(1, 2), norm='ortho')
        weight = torch.view_as_complex(self.complex_weight)
        x = x * weight
        x = torch.fft.irfft2(x, s=(H, W), dim=(1, 2), norm='ortho')
        return x

