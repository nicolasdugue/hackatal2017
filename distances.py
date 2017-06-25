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

fichier=open("vocFiltered.tsv")
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
		pass
print cpt
print error


fichier =open("vocDistance-"+lemot+".tsv", "w")
histoLeMot = freq[lemot]
categLeMot = classesnorm[lemot]
# max distance temporelle
maxDistanceTempo=0.0
for mot in dico:
	# distance = kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot)
	distance = euclide(histoLeMot, freq[mot])
	maxDistanceTempo=max(maxDistanceTempo,distance)

for mot in dico:
	# distance1 = (kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot))/maxDistanceTempo
	distance1 = euclide(histoLeMot, freq[mot])/float(maxDistanceTempo)
	# distance2 = kl(categLeMot, classesnorm[mot])+kl(classesnorm[mot],categLeMot)
	distance2 = euclide(categLeMot, classesnorm[mot])/float(len(categLeMot))
	# distanceMax = max(distance1,distance2)
	distanceMax = max(distance1,distance2)
	fichier.write(mot+" "+str(distance1)+" "+str(distance2)+" "+str(distanceMax)+"\n")
fichier.close()
