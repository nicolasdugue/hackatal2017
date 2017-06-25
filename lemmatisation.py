# coding: latin1

import sys
import numpy as np

def compteAnneeNonNulle(vecteur):
	nb = 0
	for i in range(len(vecteur)):
		if (vecteur[i]>0):
			nb+=1
	return nb

# fichier d'entrée
fichier=open("vocFiltered.tsv")
dico=set()

# mot pour le calcul de distance
cpt=0
freq=dict()
classes=dict()
classesnorm=dict()

import csv

with open('lefff-3.4.elex/lefff-3.4.elex') as d:
    reader = csv.reader(d, delimiter='\t')
    lem_dict = {row[0]: row[4].split('_', 1)[0] for row in reader}

sortie_error =open("vocLemma-notfound.tsv", "w")

error=0
for ligne in fichier:
	try:
		tab=ligne.split("\t")
		mot=tab[0].strip()
		motoriginal=mot
		mot = lem_dict.get(mot, "")
		if (len(mot)>0):
			if (mot in dico):
				freqM = np.array(map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(","))))
				np.add(freq[mot], freqM, freq[mot])
				classesM=np.array(map(int, list(tab[3].strip().strip("[").strip("]").replace(" ", "").split(","))))
				np.add(classes[mot], classesM, classes[mot])
				classesnormM=np.array(map(float, list(tab[4].strip().strip("[").strip("]").replace(" ", "").split(","))))
				np.add(classesnorm[mot], classesnormM, classesnorm[mot])
			else:
				freq[mot]=np.array(map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(","))))
				classes[mot]=np.array(map(int, list(tab[3].strip().strip("[").strip("]").replace(" ", "").split(","))))
				classesnorm[mot]=np.array(map(float, list(tab[4].strip().strip("[").strip("]").replace(" ", "").split(","))))
				dico.add(mot)
				cpt+=1
		else:
			#mot pas trouvé dans lefff
			error+=1
			sortie_error.write(motoriginal + "\t" + tab[1] + "\t" + tab[2]+ "\t" + tab[3]+ "\t" + tab[4] + "\n")
	except IndexError:
		error+=1
		sortie_error.write(motoriginal + "\t" + tab[1] + "\t" + tab[2] + "\t" + tab[3] + "\t" + tab[4] + "\n")
		pass

print cpt
print error

sortie =open("vocLemma.tsv", "w")
for mot in dico:
	sortie.write(mot + "\t" + str(list(freq[mot])) + "\t" + str(compteAnneeNonNulle(freq[mot])) + "\t" + str(list(classes[mot])) + "\t" + str(list(classesnorm[mot])) + "\n")
sortie.close()
