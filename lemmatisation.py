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
fichier=open("voc.tsv")
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
lignes=0


def heuristiqueDuDoigt(motoriginal, freqM, nbAnnee, classesM):
	# mot de 5 lettres et plus, on garde
	if (len(motoriginal)>4):
		return True
	# apparait dans 4 années ou plus on garde
	if (nbAnnee>3):
		return True
	if (np.sum(freqM)>5):
		return True
	return False


for ligne in fichier:
	lignes+=1
	try:
		tab=ligne.split("\t")
		mot=tab[0].strip()
		motoriginal=mot
		mot = lem_dict.get(mot, "")
		freqM = np.array(map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(","))))
		nbAnnee = int(tab[2])
		classesM = np.array(map(int, list(tab[3].strip().strip("[").strip("]").replace(" ", "").split(","))))
		classesnormM = np.array(map(float, list(tab[4].strip().strip("[").strip("]").replace(" ", "").split(","))))
		if (len(mot)>0) or heuristiqueDuDoigt(motoriginal,freqM,nbAnnee, classesM):
			# trouvé dans lefff ou heuristique réussie, on record
			if (mot in dico):
				np.add(freq[mot], freqM, freq[mot])
				np.add(classes[mot], classesM, classes[mot])
				#np.add(classesnorm[mot], classesnormM, classesnorm[mot])
			else:
				freq[mot]=freqM
				classes[mot]=classesM
				#classesnorm[mot]=classesnormM
				dico.add(mot)
				cpt+=1
		else:
			error+=1
			sortie_error.write(motoriginal + "\t" + tab[1] + "\t" + tab[2]+ "\t" + tab[3]+ "\t" + tab[4] + "\n")
	except IndexError:
		error+=1
		sortie_error.write(motoriginal + "\t" + tab[1] + "\t" + tab[2] + "\t" + tab[3] + "\t" + tab[4] + "\n")
		pass

print "output : "+ str(cpt)
print "erreurs : " + str(error)
print "compression : " + str(lignes-(cpt+error))

sortie =open("vocLemma.tsv", "w")
for mot in dico:
	somme=np.sum(classes[mot])
	s2=map(lambda x: x / float(somme), classes[mot])
	sortie.write(mot + "\t" + str(list(freq[mot])) + "\t" + str(compteAnneeNonNulle(freq[mot])) + "\t" + str(list(classes[mot])) + "\t" + str(list(s2)) + "\n")
sortie.close()
