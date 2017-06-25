import os
import sys
import string
annees=os.listdir("hasIpcCorr")
dicoClass=dict()
periodNumber=int(sys.argv[1])


classes=["A", 
#"C", "D", "E", "F",
 "G", "H"]
dicoClass=dict()
dicoClass["A"]=0
#dicoClass["B"]=1
#dicoClass["C"]=2
#dicoClass["D"]=3
#dicoClass["E"]=4
#dicoClass["F"]=5
dicoClass["G"]=1
dicoClass["H"]=2
classes.sort()

matrix=[]

dicoIdentifiant=dict()

cpt=0

limite=2001
limiteMin=limite + (periodNumber - 1)*2
limiteMax=limite+periodNumber*2

for annee in annees:
	fichiers=os.listdir("hasIpcCorr/"+annee)
	fichiers.sort()
	if annee > str(limiteMin) and annee < str(limiteMax):
		for f in fichiers:
			brevet=open("hasIpcCorr/"+annee+"/"+f)
			appartenance=[0] * len(dicoClass)
			for ligne in brevet:
				if ligne.startswith("code :::") or ligne.startswith("file :::") or ligne.startswith("date :::") or ligne.startswith("description :::"):
					continue
				else:
					if ligne.startswith("ipc :::"):
						if ligne.strip("ipc ::: ")[0] in dicoClass:
							appartenance[dicoClass[ligne.strip("ipc ::: ")[0] ] ]=1
			matrix.append(appartenance)
			dicoIdentifiant[cpt]="hasIpcCorr/"+annee+"/"+f
			cpt+=1
					
	
res=open("clustering"+str(periodNumber)+".mx","w")
for fichierAppartenance in matrix:
	for appartenance in fichierAppartenance:
		res.write(str(appartenance)+"\t")
	res.write("\n")
res.close()

res=open("labels"+str(periodNumber), "w")
for i in range(len(dicoIdentifiant)):
	res.write(dicoIdentifiant[i]+"\n")
res.close()
