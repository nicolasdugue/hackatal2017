#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Include the fmax file of package pyfmax using fm namespace
import pyfmax.fmaxWithMultiLabels as fm
#import numpy lib using np namespace
import numpy as np

import sys

#Load the file as a 2D array
clustering=np.loadtxt(sys.argv[2])
labels_col=[]
#Read the labels of columns (features)
labels=open("voc_freqmin50_docmax4000_classemax5")
for ligne in labels:
	labels_col.append(ligne.split("\t")[0].strip())
#Load the file as a 2D array
matrix=np.loadtxt(sys.argv[1])

#Create a MatrixClustered object using fm namespace which refers to fmax.py in package pyfmax
obj=fm.MatrixClustered(matrix, clustering,labels_col=labels_col)
obj.get_dfsl(sys.argv[1])
