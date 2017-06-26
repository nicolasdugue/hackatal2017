Nous prenons l'exemple où nous voulons étudier les évolution de mot-clé entre la période 2001/2003 et la période 2004/2006 dans le cluster A :
```
python comparaisonDecile.py specificites20012003A.dfsl specificites20042006A.dfsl
```

On obtient en sortie les mots clés stables entre les deux périodes et ceux qui burstent

En regardant Cmp_specificites20012003A.dfsl_specificites20042006A.dfsl qui a été créé par la commande, on peut regarder les évolutions pour chaque mot :
```
head Cmp_specificites20012003A.dfsl_specificites20042006A.dfsl 
trifluorométhoxy	0	0	0	0.00200580628134
alkyléthersulfates	0	0	0	0.00198471348338
exponentiation	0	0	0	0.00126729327278
```
L'ordre des colonnes est comme suit :
décile en première période, décile en seconde période, variation du décile entre les deux périodes, feature f-mesure en premier période

Les mots ci-dessus sont tous dans le décile 0 (le premier), ils sont donc importants

