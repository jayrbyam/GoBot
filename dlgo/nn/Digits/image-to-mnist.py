from PIL import Image
from numpy import genfromtxt
import gzip
import six.moves.cPickle as cPickle
from glob import glob
import numpy as np
import pandas as pd

def files_to_dataset(glob_files, train=False):
    dataset = []
    for file_name in sorted(glob(glob_files), key=len):
        img = Image.open(file_name).convert('LA') #tograyscale
        pixels = [f[0] / 255 for f in list(img.getdata())]
        dataset.append(pixels)
    labels = []
    if not train:
        labels = [0,1,2,3,4,5,6,7,8,9] * 13
    else:
        for i in range(10):
            labels.extend([i]*13)
    return np.array(dataset), np.array(labels)

Data1, y1 = files_to_dataset("Digits/trains/*/*.jpg", train=True)
Data2, y2 = files_to_dataset("Digits/test/*.jpg")

train_set = Data1, y1
test_set = Data2, y2
dataset = train_set, test_set

f = gzip.open('mine.pkl.gz','wb')
cPickle.dump(dataset, f, protocol=2)
f.close()