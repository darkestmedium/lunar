# Built-in imports
# Temp override for vs code
import sys
sys.path.append("./python/310/packages")

# Third-party imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from keras import layers, losses
from keras.datasets import fashion_mnist
from keras.models import Model

# Custom imports

filePathAnim = "/Users/luky/My Drive/Development/3d/Maya/LunarDev/deep/data/ecg.csv"
filePathEcg = "/Users/luky/My Drive/Development/3d/Maya/LunarDev/deep/data/as_p_scout_idle_to_walk_180r_foot_r.json"

dataframe = pd.read_csv(filePathEcg, header=None)
raw_data = dataframe.values
dataframe.head()