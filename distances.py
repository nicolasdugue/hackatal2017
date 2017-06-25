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
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    return np.sum( p * np.log((p+1) / (q+1)))

fichier=open("vocFiltered.tsv")
dico=set()

# mot pour le calcul de distance
lemot = sys.argv[1]
cpt=0
freq=dict()
nbAnnee=dict()


error=0
for ligne in fichier:
	try:
		tab=ligne.split("\t")
		mot=tab[0].strip()
		freq[mot]=map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(",")))
		nbAnnee[mot]=int(tab[2])
		dico.add(mot)
		cpt+=1
	except IndexError:
		error+=1
		pass
print cpt
print error

fichier =open("vocDistance-"+lemot+".tsv", "w")
histoLeMot = freq[lemot]
for mot in dico:
	distance = kl(histoLeMot, freq[mot])+kl(freq[mot], histoLeMot)
	fichier.write(mot+" "+str(distance)+"\n")
fichier.close()
