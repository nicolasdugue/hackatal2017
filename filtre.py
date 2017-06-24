import sys

fichier=open("voc.tsv")
dico=dict()

borneMin=int(sys.argv[1])
borneMax=int(sys.argv[2])
cpt=0

print borneMin, borneMax
for ligne in fichier:
	tab=ligne.split("\t")
	freq=int(tab[1].strip())
	dico[tab[0]]=freq
	if freq > borneMin and freq < borneMax:
		cpt+=1
print cpt
