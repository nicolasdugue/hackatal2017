# -*- coding: utf-8 -*-

import numpy as np
import operator
import sys

fichier1=open(sys.argv[1])
fichier2=open(sys.argv[2])

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

fichier=open("Cmp_"+sys.argv[1]+"_"+sys.argv[2], "w")
print("--------Mots stables très représentatifs----------\n\n")
for mot in liste:
	mot,perc1,perc2,diff=mot
	if perc1 == 0 and perc2 == 0:
		print(mot)
	fichier.write(mot+"\t"+str(perc1)+"\t"+str(perc2)+"\t"+str(diff)+"\t"+str(dico1[mot])+"\n")
fichier.close()

print("\n\n--------Mots qui burst----------\n\n")
for mot in liste:
	mot,perc1,perc2,diff=mot
	if perc1 > 1 and perc2 == 0:
		print(mot)

