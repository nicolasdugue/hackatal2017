#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.sparse import csr_matrix, csc_matrix
import numpy as np
from math import pow
import operator

class MatrixClustered:
	"""
		This class allows to define a matrix which rows (objects) were clustered
		Labels can be used to describe rows (objects) and columns (features)
    	"""

	def __init__(self, matrix, clustering, labels_row=[], labels_col=[]):
		"""
		Matrix and clustering should be at least passed.
		Matrix should be a 2D Array or already a sparse (csr or csc) matrix.
		Clustering should be a 2D binary Array where a value 1 at index i,j defines that the object i (row i in matrix) belongs to cluster j
		Labels can be used to describe rows (objects) and columns (features) in the same way as the clustering object
    		"""

		self.matrix_csr = csr_matrix(matrix)

		self.matrix_csc = csc_matrix(matrix)

		self.clustering=clustering
		
		self.clusters=[]
		for i,binaryListClusters in enumerate(self.clustering):
			for j, boolean in enumerate(binaryListClusters):
				taille=(len(self.clusters) -1) 
				if j >= taille:
					for i in range(j - taille):
						self.clusters.append([])
				self.clusters[j].append(i)

		self.labels_row=labels_row

		self.labels_col=labels_col

		self.sum_rows=self.matrix_csr.sum(axis=1)

		self.sum_cols=self.matrix_csc.sum(axis=0)
		
		self.ffmean=np.empty(self.matrix_csr.shape[1])
		self.ffmean.fill(-1.0)
		
		self.features_selected=[]
		

		

	def sum_row(self, i):
		"""
		Get the sum of row i
    		"""
		return self.sum_rows[i]

	def sum_col(self, j):
		"""
		Get the sum of column j
		Used in Feature Precision (Predominance)
    		"""
		return self.sum_cols[:,j]
	
	def sum_col_of_cluster(self, j, k):
		"""
		Get the sum of column j
		Used in Feature Precision (Predominance)
    		"""
		column=self.matrix_csc.getcol(j).toarray();
		som=0
		for idx,elmt in enumerate(column):
			if (self.clustering[idx][k] == 1):
				som+=elmt
		return som	
	
	def sum_cluster(self, i):
		"""
		Get the sum of cluster i
		Used in feature recall
    	"""   	
		cluster=self.clusters[i]
		som=0
		for row in cluster:
			som+=self.sum_row(row)
		return som
	
	def fp(self, j, k):
		"""
		Get the feature precision (or predominance) of feature j in cluster k
    	"""
		numerator=self.sum_col_of_cluster(j, k)
		denominator =self.sum_cluster(k)
		if denominator == 0:
			return 0
		else:
			return numerator / denominator
		
	def fr(self, j, k):
		"""
		Get the feature recall of feature j in cluster k
    	"""
		numerator=self.sum_col_of_cluster(j, k)
		denominator =self.sum_col(j)
		if denominator == 0:
			return 0
		else:
			return numerator / denominator
	
	def ff(self, j, k):
		"""
		Get the feature f measure of feature j in cluster k
    	"""
		fr=self.fr(j,k)
		fp=self.fp(j,k)
		if fr == 0 and fp == 0:
			return 0
		else:
			return (2*fr*fp) /(fr + fp) 
		
	def ff_mean(self, j):
		"""
		Get the mean value of feature f-measure for feature j across all clusters
    	"""
		mean=0
		for k in range(len(self.clusters)):
			mean+=self.ff(j,k)
		self.ffmean[j]=mean / len(self.clusters)
		return self.ffmean[j]
	
	def contrast(self, j,k):
		"""
		Get the contrast of feature j in cluster k
    	"""
		return self.ff(j, k) / self.ff_mean(j)
	
	def ff_mean_all(self):
		"""
		Get the mean value of feature f-measure for all features
    	"""
		mean=0
		for j in range(self.get_cols_number()):
			if (self.ffmean[j] == -1):
				self.ff_mean(j)
			mean+=self.ffmean[j]
		return mean / self.get_cols_number()
			
		
	def get_row_label(self, i):
		"""
		Get the label of row i
    	"""
		if len(self.labels_row) == len(self.clustering):
			return self.labels_row[i]
		else:
			return i+""
		
	def get_col_label(self, j):
		"""
		Get the label of col j
    	"""
		if len(self.labels_col) > 0:
			return self.labels_col[j]
		else:
			return j+""
		
	def get_features_selected(self):
		'''
		Return for each cluster the set of features selected
		'''
		if len(self.features_selected) == 0:
			for k in range(self.get_clusters_number()):
				print("k",k)
				selected=[]
				for j in range(self.get_cols_number()):
					ff=self.ff(j, k)
					if ff >= self.ff_mean(j) and ff >= self.ff_mean_all():
						selected.append(j)
					if (j % 10) == 0:
						print "j",j
				self.features_selected.append(selected)
		return self.features_selected
	
	def get_features_selected_flat(self):
		'''
		Return an array of the feactures selected for the whole dataset, namely all the classes
		'''
		fs=self.get_features_selected()
		fs_flat=[item for sublist in fs for item in sublist]
		return set(fs_flat)
	
	def get_rows_number(self):
		"""
		Get the number of rows
    	"""
		return self.matrix_csr.shape[0]
	
	def get_cols_number(self):
		"""
		Get the number of cols
    	"""
		return self.matrix_csr.shape[1]
	
	def get_cluster(self, k):
		return self.clusters[k]
	
	def get_size_cluster(self, k):
		return len(self.get_cluster(k))
	
	def get_clusters_number(self):
		"""
		Get the number of cols
    	"""
		return len(self.clusters)
	
	def get_dfsl(self,fichier):
		for k in range(self.get_clusters_number()):
			fichierE=open(fichier+str(k)+".dfsl", "w")
			liste=[]
			for j in range(self.get_cols_number()):
				liste.append((self.get_col_label(j), float(self.ff(j, k))))
			liste.sort(key=operator.itemgetter(1))
			for obj in liste:
				mot, ff=obj
				fichierE.write(mot+"\t"+str(ff)+"\n")
			fichierE.close()

	def __str__(self):
		"""
		toString()
    		"""
		return "Matrix CSR (ordered by rows) :\n" + str(self.matrix_csr)+ "\nMatrix CSC (ordered by columns): \n"+ str(self.matrix_csc) + "\nColumns labels (features) " + str(self.labels_col) + "\nRows labels (objects) " + str(self.labels_row) + "\nClustering :  " + str(self.clustering)+"\nClusters : "+str(self.clusters)
		
