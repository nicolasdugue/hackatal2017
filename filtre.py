import sys
import numpy as np

fichier=open("voc.tsv")
dico=set()

borneMin=int(sys.argv[1])
borneMax=int(sys.argv[2])
cpt=0

error=0
print borneMin, borneMax
for ligne in fichier:
	try:
		tab=ligne.split("\t")
		mot=tab[0]
		freq=map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(",")))
		nbAnnee=int(tab[2])
		docTotal=np.sum(np.array(freq))
		if not mot.isdigit() and nbAnnee > 1 and docTotal > borneMin and docTotal < borneMax:
			dico.add(tab[0].strip())
			cpt+=1
	except IndexError:
		error+=1
		pass
print cpt
print error
fichier =open("voc_freqmin"+str(borneMin)+"_freqmax"+str(borneMax), "w")
for mot in dico:
	fichier.write(mot+"\n")
fichier.close()
