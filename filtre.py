import sys

fichier=open("voc.tsv")
dico=set()

borneMin=int(sys.argv[1])
borneMax=int(sys.argv[2])
ratio=float(sys.argv[3])
cpt=0

error=0
print borneMin, borneMax
for ligne in fichier:
	try:
		tab=ligne.split("\t")
		freq=int(tab[1].strip())
		dico.add(tab[0].strip())
		rtio= float(tab[2]) / 120000
		if freq > borneMin and freq < borneMax and rtio < ratio:
			cpt+=1
	except IndexError:
		error+=1
		pass
print cpt
print error
fichier =open("voc_freqmin"+str(borneMin)+"_freqmax"+str(borneMax)+"_ratiomax"+str(ratio), "w")
for mot in dico:
	fichier.write(mot+"\n")
fichier.close()
