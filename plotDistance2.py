#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pylab as py

# coding: latin1

import sys
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

fichier=open("voc.tsv")
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
		print ligne
		pass
print cpt
print error


fichier =open("vocDistance-"+lemot+".tsv", "w")
histoLeMot = freq[lemot]
categLeMot = classesnorm[lemot]
# max distance temporelle
maxDistanceTempo=0.0
#for mot in dico:
	# distance = kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot)
#	distance = euclide(histoLeMot, freq[mot])
#	maxDistanceTempo=max(maxDistanceTempo,distance)

data=[10,10,10,10,10,10,10,10,10,10]
for mot in dico:
	# distance1 = (kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot))/maxDistanceTempo
	distance1 = euclide(histoLeMot, freq[mot])/float(maxDistanceTempo)
	# distance2 = kl(categLeMot, classesnorm[mot])+kl(classesnorm[mot],categLeMot)
	distance2 = euclide(categLeMot, classesnorm[mot])/float(len(categLeMot))
	# distanceMax = max(distance1,distance2)
	distanceMax = max(distance1,distance2)
	for idx,d in enumerate(data):
		mot,d1,d2,dMax=d
		if dMax < d:
			for j in reverse(range(idx, len(data))):
				data[j]=data[j-1]
			data[idx]=(mot, distance1, distance2, distanceMax)
			break
print data
			

data = [["tactile", 0.0, 0.0, 0.0],
        ["affiche",4.22182432007e-05,0.000120576977518,0.000120576977518],
        ["cadran", 0.000133922627135, 0.000147346167705, 0.000147346167705],
        ["pictogrammes", 0.000154609169406, 0.000135689862641, 0.000154609169406],
        ["modelisations", 0.000162408209466, 0.00013212070719, 0.000162408209466],
        ["apodisation", 0.000164872477325, 0.000166276546644, 0.000166276546644],
        ["pointees", 0.000163521857755, 0.000183796628625, 0.000183796628625],
        ["balaie", 0.000160267296508, 0.000183799033322, 0.000183799033322],
        ["afficheur",5.23671511913e-05, 0.000189541918042, 0.000189541918042]]

for item in data:
	py.scatter(item[1]*1000, item[2]*10000, s=70000000*item[3], c=(item[2], 0, 1 - item[2]), marker=r"$ {} $".format(item[0]), edgecolors='none' )
py.show()
