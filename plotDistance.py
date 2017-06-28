#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pylab as py

# coding: latin1

import sys
import matplotlib.pyplot as plt
import numpy as np


def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    return np.sum(np.where(p != 0, p * np.log((p+1) / (q+1)), 0))


def euclide(p, q):
    total = 0
    for idx, value in enumerate(p):
       total += (value-q[idx])*(value-q[idx])
    return total

def get_distance(p,q):
	return euclide(p,q)

fichier=open("vocLemma.tsv")
dico=set()

# mot pour le calcul de distance
lemot = sys.argv[1]
# lemot = "karaoké"
cpt=0
freq=dict()
nbAnnee=dict()
classes=dict()
classesnorm=dict()

error=0
for ligne in fichier:
	try:
		tab=ligne.split("\t")
		mot=tab[0].strip()
		freq[mot]=map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(",")))
		nbAnnee[mot]=int(tab[2])
		classes[mot]=map(int, list(tab[3].strip().strip("[").strip("]").replace(" ", "").split(",")))
		classesnorm[mot]=map(float, list(tab[4].strip().strip("[").strip("]").replace(" ", "").split(",")))
		dico.add(mot)
		cpt+=1
	except IndexError:
		error+=1
		#print ligne
		pass
#print cpt
#print error


histoLeMot = freq[lemot]
categLeMot = classesnorm[lemot]
# max distance temporelle
maxDistanceTempo=0.0
for mot in dico:
	# distance = kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot)
	distance = get_distance(histoLeMot, freq[mot])
	maxDistanceTempo=max(maxDistanceTempo,distance)

data=[("a",1000,10000,10000),("a",1000,10000,10000),("a",1000,10000,10000),("a",1000,10000,10000),("a",1000,10000,10000),("a",1000,10000,10000)]
for mot in dico:
	# distance1 = (kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot))/maxDistanceTempo
	distance1 = get_distance(histoLeMot, freq[mot])/float(maxDistanceTempo)
	# distance2 = kl(categLeMot, classesnorm[mot])+kl(classesnorm[mot],categLeMot)
	distance2 = get_distance(categLeMot, classesnorm[mot])/float(len(categLeMot))
	# distanceMax = max(distance1,distance2)
	distanceMax = max(distance1,distance2)
	for idx,d in enumerate(data):
		mot2,d1,d2,dMax=d
		if distanceMax < dMax:
			for j in reversed(range(idx, len(data))):
				data[j]=data[j-1]
			data[idx]=(mot, distance1, distance2, distanceMax)
			break
#print data
			

plt.subplot(1, 2, 1)
forHistoTime=[]
forHistoClass=[]
names=[]
for item in data:
	try:
		plt.scatter(item[1]*1000, item[2]*1000, s=5000, c=(item[2], 0, 1 - item[2]), marker=r"$ {} $".format(item[0]), edgecolors='none' )
		names.append(item[0])
		forHistoTime.append(freq[item[0] ])
		forHistoClass.append(classesnorm[item[0] ])
	except: 
		pass
plt.xlabel('Distance sur la distribution dans les annees')
plt.ylabel('Distance sur la distribution dans les catego')

time_plt=plt.subplot(2, 2, 2)

classes=range(2001,2016)
bar_width = 5
classes_x = bar_width*(len(data)+1)*np.arange(len(classes))
time_plt.set_xticks(classes_x, minor=False)
time_plt.set_xticklabels(classes, minor=False)

cmap = plt.get_cmap('jet')
colors = cmap(np.linspace(0, 1.0, len(names)))

for i, item in enumerate(names):
	plt.bar(classes_x+i*bar_width, forHistoTime[i], width=bar_width, color=colors[i], label=item)
plt.legend()
plt.ylabel('Nombre de documents ou le mot apparait dans l\'annee')

classes_plt=plt.subplot(2, 2, 4)
classes = 'ABCDEFGH'

classes_x = bar_width*(len(data)+1)*np.arange(len(classes))
classes_plt.set_xticks(classes_x, minor=False)
classes_plt.set_xticklabels(classes, minor=False)


for i, item in enumerate(names):
	plt.bar(classes_x+i*bar_width, forHistoClass[i], width=bar_width, color=colors[i], label=item)
plt.legend(loc = 'best')

plt.ylabel('Nombre de documents ou le mot apparait dans la classe')
plt.show()
