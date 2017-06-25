import numpy as np
import operator

fichier1=open("specificites20012002A.dfsl")
fichier2=open("specificites20032004A.dfsl")

values1=[]
dico1=dict()
values2=[]
dico2=dict()

for ligne in fichier1:
	tab=ligne.split("\t")
	mot,val=tab
	mot=mot.strip()
	val=float(val.strip())
	values1.append(val)
	dico1[mot]=val


for ligne in fichier2:
	tab=ligne.split("\t")
	mot,val=tab
	mot=mot.strip()
	val=float(val.strip())
	values2.append(val)
	dico2[mot]=val

dicoPerc1=dict()
dicoPerc2=dict()

percentiles1=[]
for i in reversed(range(1,9)):
	percentiles1.append(np.percentile(values1, i*10))
print percentiles1
percentiles2=[]
for i in reversed(range(1,9)):
	percentiles2.append(np.percentile(values2, i*10))

for mot in dico1:
	val=dico1[mot]
	for idx,perc in enumerate(percentiles1):
		if val > perc:
			dicoPerc1[mot]=idx
			break
	if mot not in dicoPerc1:
		dicoPerc1[mot]=10

for mot in dico2:
	val=dico2[mot]
	for idx,perc in enumerate(percentiles2):
		if val > perc:
			dicoPerc2[mot]=idx
			break
	if mot not in dicoPerc2:
		dicoPerc2[mot]=10
liste=[]
for mot in dicoPerc1:
	if mot not in dicoPerc2:
		liste.append((mot, dicoPerc1[mot], 10, dicoPerc1[mot]-10))
	else:	
		liste.append((mot, dicoPerc1[mot], dicoPerc2[mot], dicoPerc1[mot]-dicoPerc2[mot]))
liste.sort(key=operator.itemgetter(1))

fichier=open("ComparaisonA1erePeriode", "w")
for mot in liste:
	mot,perc1,perc2,diff=mot
	fichier.write(mot+"\t"+str(perc1)+"\t"+str(perc2)+"\t"+str(diff)+"\n")
fichier.close()


